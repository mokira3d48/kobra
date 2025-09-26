import os
from datetime import datetime, timezone
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model
from django.db import models

ALLOWED_EXTENSIONS = ['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png']
User = get_user_model()


def upload_path(instance: models.Model, filename: str) -> str:
    """Generate a unique upload path for document files.

    Creates an organized folder structure to prevent filename collisions
    and group files by user and upload time. The path follows the pattern:
    ``documents/user_<user_id>/<timestamp>_<original_filename>``

    :param instance: The Document model instance being saved. Must have
      an author attribute with an id field.
    :param filename: The original filename of the uploaded file.
    :return: A relative path string for file storage.

    :example:
        >>> upload_path(document_instance, "report.pdf")  # noqa
        'documents/user_42/20231215_143022_report.pdf'

    :seealso:
        :class:`Document` - The model that uses this upload path function
    """
    current_time = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
    user_folder = f"user_{instance.author.id}"  # noqa
    return os.path.join("documents", user_folder, f"{current_time}_{filename}")


class Document(models.Model):
    """Represents a document uploaded by a user in the system.

    Stores metadata about the document including title, file reference,
    timestamps, and authorship. The actual file is stored using the
    FileField with custom validation and storage path.

    * title: Human-readable title for the document (128 char limit).
    * file: The actual file with restrictions:
      - Custom upload path function determines storage location.
      - Validates file extension against allowed types.
      - Verbose name "file" for admin/displays.
    * created_at: Automatically set to current timestamp when document
      is created (immutable).
    * updated_at: Automatically updated to current timestamp on every save.
    * author: Reference to the user who uploaded this document
      If user is deleted, all their documents are deleted (CASCADE).
    """
    title = models.CharField("title", max_length=128)
    file = models.FileField(
        upload_to=upload_path, verbose_name="file",
        validators=[FileExtensionValidator(ALLOWED_EXTENSIONS)]
        )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        to=User, on_delete=models.CASCADE, verbose_name="author"
        )

    class Meta:
        """
        Metadata options for the Document model.

        * verbose_name: Human-readable singular name for admin.
        """
        verbose_name = "Document"

    def __str__(self) -> str:
        """
        Human-readable string representation of the document.
        Format: "document #123 - author: john_doe - title: Report.pdf"
        """
        return (
            f"document #{self.pk} "
            f"- author: {self.author.username} "   # noqa
            f"- title: {self.title}"
            )
