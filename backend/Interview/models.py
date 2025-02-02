from django.db import models
class Interview(models.Model):
    interview_id = models.AutoField(primary_key=True)
    candidate = models.ForeignKey("ApplyPage.Candidate", on_delete=models.CASCADE, related_name="interviews")
    job_role = models.CharField(max_length=255)
    total_score = models.IntegerField(default=0, verbose_name="Total Interview Score")
    video_call_path = models.URLField(verbose_name="Video Call Recording Path", null=True, blank=True)
    interview_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Interview {self.interview_id} - {self.candidate.name}"


class Response(models.Model):
    response_id = models.AutoField(primary_key=True)
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE, related_name="responses")
    question = models.ForeignKey("dashboard.Question", on_delete=models.CASCADE)
    response_text = models.TextField()
    score = models.IntegerField()
    
    def __str__(self):
        return f"Response for question: {self.question.question_id} in Interview {self.interview.interview_id}"
