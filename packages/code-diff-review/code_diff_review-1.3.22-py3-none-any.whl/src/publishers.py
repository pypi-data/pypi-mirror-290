import os
import re
from typing import List, Optional, Dict, Any
from cururo.util.publisher import Publisher
from github import Github, Auth, GithubException
from github.Issue import Issue

class MermaidPrivate:
    def __init__(self, pattern=r'```mermaid\n(.*?)\n```', types='journey'):
        self.pattern=pattern
        self.types=types

    def generate_journey(self, title, to_add:str, body=''):
        code, exists = self.get_mermaid_code(title, body)
        code = self.append2mermaid(code, to_add)
        return self.insert_code(body, code, exists)

    def journey(self, title):
        return f'journey\ntitle {title}'

    def insert_code(self, body: str, mermaid_code: str, replace=True) -> str:
        if replace:
            # Replace existing Mermaid code
            return re.sub(self.pattern, f'```mermaid\n{mermaid_code}\n```', body, flags=re.DOTALL)
        else:
            # Append Mermaid code at the end if pattern doesn't exist
            return body + f'\n```mermaid\n{mermaid_code}\n```'

    def get_mermaid_code(self, title: str, body: str):
        match = re.search(self.pattern, body, re.DOTALL)
        if match:
            return match.group(1), True
        return self.journey(title), False

    def dict2section(self, section: str, steps: Dict[str, str], who: str) -> str:
        section_str = f'section {section}\n'
        for step, value in steps.items():
            section_str += f'{step}: {value}: {who}\n'
        return section_str
    
    def append2mermaid(self, mermaid: str, data: str) -> str:
        return f'{mermaid}\n{data}'

class GitIssuePublisher(Publisher):
    """
    A class to publish and manage GitHub issues with branch-specific threading and graph updates.
    """

    def __init__(self, _api_key: str, repo: str, branch: str, sha: str):
        """
        Initializes the GitIssuePublisher with authentication, repository, and branch details.

        :param _api_key: The GitHub API key for authentication.
        :param repo: The name of the GitHub repository.
        :param branch: The name of the branch related to the issue.
        :param sha: The commit SHA related to the issue.
        """
        super().__init__()

        try:
            _auth = Auth.Token(_api_key)
            self.__github = Github(auth=_auth)
            self.repo = repo
            self.branch = branch
            self.sha = sha
            self.user = self.__github.get_user().login
        except GithubException as e:
            raise Exception(f"Error initializing GitHub client: {e}")

    def __get_repo(self):
        """
        Retrieves the GitHub repository object.

        :return: The GitHub repository object.
        """
        try:
            return self.__github.get_repo(self.repo)
        except GithubException as e:
            raise Exception(f"Error retrieving repository {self.repo}: {e}")


    def publish(self, data):
        """
        Publishes or updates an issue with the graph and body content.

        :param data: The body for the issue.
        :return: None
        """
        try:
            title = f"Automated Issue on branch {self.branch}"
            print(1)
            existing_issue = self.get_thread(title)

            print(2)
            updated_body = self.generate_issue(existing_issue.body or '', 
                                                        message=data['message']['adherence']['score'],
                                                        vulnerability=data['codeVulnerability']['score'])
            print(3)
            existing_issue.edit(body=updated_body)
            print(4)
            existing_issue.create_comment(self.generate_report(data))

            return 
        except GithubException as e:
            raise Exception(f"Error publishing issue: {e}")
 
    def get_thread(self, title: str, body: Optional[str] = ''):
        """
        Searches for an issue by title and creates or reopens it if necessary.

        :param title: The title of the issue to search or create.
        :param body: The body text for a new issue.
        :return: The existing or newly created issue.
        """
        try:
            repo = self.__get_repo()

            ############################################################################
            # Search for the issue by title
            # Esta parte del codigo es la mas costosa... investigar como optimizar
            issues = repo.get_issues(state='all')  # Fetch all issues (open and closed)
            existing_issue = next((issue for issue in issues if issue.title == title), None)
            ############################################################################

            # Check if the issue is found
            if existing_issue:
                if existing_issue.state != 'open':
                    existing_issue.edit(state='open')
                existing_issue.add_to_assignees(self.user)
                return existing_issue

            # If no issue is found, create a new one
            # This creates the first comment... this is where we are going to have the summary built with markdown
            new_issue = repo.create_issue(title=title, body=body, assignee=self.user)
            return new_issue

        except GithubException as e:
            raise Exception(f"Error threading issue: {e}")

    def generate_report(self, data):
        report = [
            f"### Commit Review Summary [{self.sha}]\n",
            f"**Author:** {self.user}\n",
            f"**Message:**\n",
            f"- **Provided:** {data['message']['provided']}",
            f"- **Generated:** {data['message']['generated']}\n",
            f"- **Adherence Score:** {data['message']['adherence']['score']} {data['message']['adherence']['emoji']}",
            f"  *{data['message']['adherence']['comment']}*\n",
            "\n**Code Complexity:**\n",
            f"- **Comment:** {data['codeComplexity']['comment']}\n",
            "\n**Code Vulnerability:**\n",
            f"- **Score:** {data['codeVulnerability']['score']} {data['codeVulnerability']['emoji']}",
            f"  *{data['codeVulnerability']['comment']}*\n",
            "\n**SOLID Principles Analysis:**\n",
            "| Principle            | Score | Comment |\n",
            "|----------------------|-------|---------|\n"
        ]

        for principle, details in data['codeSOLID'].items():
            report.append(
                f"| {principle.replace('_', ' ').title()} | {details['score']} {details['emoji']} | *{details['comment']}* |"
            )

        return '\n'.join(report)

    def generate_issue(self, existing_body: str, **scores) -> str:
        """
        Appends adherence data to the existing comment body using a Mermaid XY diagram.

        :param existing_body: The existing comment body.
        :param adherence: A dictionary with adherence score details.
        :return: The updated comment body.
        """
        mermaid = MermaidPrivate()
        data = mermaid.dict2section(self.sha, scores, self.user)
        return mermaid.generate_journey("Scores History", data, existing_body)

    
class WebPublisher(Publisher):

    def __init__(self, url:str, secret:str):
        super().__init__()
        self.url = url
        self.secret = secret

    def publish(self, data):
        return self.__send_request(data)

    def __send_request(self, data):
        headers = { 'Content-Type': 'application/json' }
        data['secret'] = self.secret
        res = requests.post(self.url, headers=headers, json=data)
        res.raise_for_status()
        return res

    def sort_data(self, data: Dict[str, Any], others: Dict[str, Any] = None) -> Dict[str, Any]:
        if others is None:
            others = {}
        sorted_data = {
            'message': data['message'].get('message', ''),
            'suggested': data['message'].get('suggested', ''),
            'adherence': data['message'].get('adherence', ''),
            'completeness': data['message'].get('completeness', ''),
            'atomicity': data['code']['acid_score'].get('a', ''),
            'consistency': data['code']['acid_score'].get('c', ''),
            'isolation': data['code']['acid_score'].get('i', ''),
            'durability': data['code']['acid_score'].get('d', ''),
            'vulnerability': data['code']['vulnerable_code'].get('score', ''),
        }
        sorted_data.update(others)
        return sorted_data


if __name__ == "__main__":
    repo = 'agustin-rios/code-diff-review'
    token = ''
    sha = 'azwexrshnuijmk'
    git_publisher = GitIssuePublisher(token, repo, sha)
    git_publisher.publish('hola')
    