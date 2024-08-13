import re
import uuid
from typing import List
from urllib.request import urlopen

from fastapi.exceptions import HTTPException
from gitlab import Gitlab
from gitlab.exceptions import GitlabAuthenticationError, GitlabCreateError
from gitlab.v4.objects.issues import ProjectIssue
from loguru import logger

from keystone_gitlab.models import IssuePayload
from keystone_gitlab.settings import GitlabSettings


def get_gl(settings: GitlabSettings) -> Gitlab:
    return Gitlab(settings.url, private_token=settings.token)


async def create_gitlab_issue_from_3rd_party(
        origin: str,
        user_display_name: str,
        user_email: str,
        payload: IssuePayload,
        settings: GitlabSettings
) -> str:
    """
    Creates a gitlab issue in behalf of the user making the request
    :param user_email:
    :param user_display_name:
    :param origin: Origin Header from request
    :param payload: IssuePayload
    :param settings: Gitlab Service Settings
    :return: Web url to gitlab issue that was created
    """
    issue_title = f"{payload.title} (submitted by {user_email})"
    issue_text = f"> Submitted by {user_display_name} ({user_email}) from {origin} \n\n {payload.text}"

    try:
        new_issue = await create_issue(issue_title, issue_text, payload.labels, settings)

        return new_issue.web_url
    except GitlabCreateError as e:
        details = e.response_body
        if isinstance(e.error_message, dict):
            parts = [f"{k} {v}" for k, v in e.error_message.items()]
            details = " | ".join(parts)

        raise HTTPException(status_code=e.response_code, detail=details)


async def create_issue(
        title: str, description: str, labels: List[str], settings: GitlabSettings,
) -> ProjectIssue:
    try:
        gl = get_gl(settings)
        # get img tags from description
        img_pattern = r'<img.*?src="(.*?)".*?>'
        matches = re.findall(img_pattern, description)
        project = gl.projects.get(settings.project_id)

        images = list(matches)
        if images:
            images_key = uuid.uuid4()
            uploaded_files = []
            for ndx, match in enumerate(matches):
                with urlopen(match) as image_data:
                    obj = project.upload(
                            filename=f"{images_key}-{ndx}.png", filedata=image_data.read()
                    )
                    uploaded_files.append(obj)

            for file in uploaded_files:
                description = re.sub(
                        img_pattern,
                        f'See the image: {file["markdown"]}',
                        description,
                        count=1,
                )
        issue: ProjectIssue = project.issues.create(
                {
                        "title": title,
                        "description": description,
                        "labels": ",".join(labels),
                }
        )
        logger.info(f"Created issue: {issue.id}")
        return issue
    except GitlabCreateError as e:
        logger.error(f"{e}")
        logger.error("Could not create issue")
        raise e
    except GitlabAuthenticationError as e:
        logger.error(f"{e}")
        logger.error("Could not authenticate with gitlab")
        raise e


if __name__ == "__main__":
    create_issue(
            "Test Bug -- ignore", "## Test \n\n testing markdown", [],
            GitlabSettings(project_id="developers/miscellaneous", token="")
    )
