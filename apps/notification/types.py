from django.db import models


class NOTIFICATION_TYPES(models.TextChoices):
    ANNOUNCEMENT = "announcement"
    NEW_VACANCY = "new_vacancy"
    NEW_FINAID_ADVERT = "new_finaid_advert", "Financial Assistance Advert"
    NEW_FINAID_APPLICATION = (
        "new_finaid_application",
        "Financial Assistance Application",
    )
    FINAID_APPROVAL = "new_finaid_approval", "Financial Assistance Approval"
    FINAID_REJECTION = "new_finaid_rejection", "Financial Assistance Rejection"
    FINAID_REVIEW = "new_finaid_review", "Financial Assistance Review"
    APPLICATION_SUBMITTED = "application_submitted", "Application Submitted"
    APPLICATION_ACCEPTED = "application_accepted", "Application Accepted"
    APPLICATION_REJECTED = "application_rejected", "Application Rejected"
    INTERVIEW_SCHEDULED = "interview_scheduled", "Interview Scheduled"
    INTERVIEW_ACCEPTED = "interview_accepted", "Interview Accepted"
    INTERVIEW_CANCELLED = "interview_cancelled", "Interview Cancelled"
