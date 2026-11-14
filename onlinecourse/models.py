from django.db import models
from django.conf import settings
from django.utils.timezone import now


# Instructor Model
class Instructor(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    full_time = models.BooleanField(default=True)
    total_learners = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} (Instructor)"


# Learner Model
class Learner(models.Model):
    STUDENT = 'student'
    DEVELOPER = 'developer'
    DATA_SCIENTIST = 'data_scientist'
    DATABASE_ADMIN = 'dba'
    OCCUPATION_CHOICES = [
        (STUDENT, 'Student'),
        (DEVELOPER, 'Developer'),
        (DATA_SCIENTIST, 'Data Scientist'),
        (DATABASE_ADMIN, 'Database Admin'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    occupation = models.CharField(
        max_length=20,
        choices=OCCUPATION_CHOICES,
        default=STUDENT
    )
    social_link = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.occupation}"


# Course Model
class Course(models.Model):
    name = models.CharField(null=False, max_length=200, default='online course')
    image = models.ImageField(upload_to='course_images/', null=True, blank=True)
    description = models.CharField(max_length=1000)
    pub_date = models.DateField(null=True, blank=True)
    instructors = models.ManyToManyField(Instructor)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Enrollment')
    total_enrollment = models.IntegerField(default=0)
    is_enrolled = False

    def __str__(self):
        return f"Course: {self.name}"


# Lesson Model
class Lesson(models.Model):
    title = models.CharField(max_length=200, default="Lesson Title")
    order = models.IntegerField(default=0)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f"{self.course.name} - Lesson {self.order}: {self.title}"


# Enrollment Model (Through model for Course <-> User)
class Enrollment(models.Model):
    AUDIT = 'audit'
    HONOR = 'honor'
    COURSE_MODES = [
        (AUDIT, 'Audit'),
        (HONOR, 'Honor'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField(default=now)
    mode = models.CharField(max_length=10, choices=COURSE_MODES, default=AUDIT)
    rating = models.FloatField(default=5.0)

    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.name}"


# Question Model
class Question(models.Model):
    # Foreign key relationship to Course
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    # Question text
    question_text = models.CharField(max_length=500)
    # Question grade / score points
    grade = models.IntegerField(default=50)

    def __str__(self):
        return f"Question: {self.question_text} ({self.grade} pts)"

    def is_get_score(self, selected_ids):
        """
        Check if the selected choice IDs earn the score for this question.
        Returns True if all correct choices were selected and no incorrect choice was selected.
        """
        all_answers = self.choice_set.filter(is_correct=True).count()
        selected_correct = self.choice_set.filter(is_correct=True, id__in=selected_ids).count()
        selected_incorrect = self.choice_set.filter(is_correct=False, id__in=selected_ids).count()

        if all_answers > 0 and all_answers == selected_correct and selected_incorrect == 0:
            return True
        return False


# Choice Model
class Choice(models.Model):
    # Foreign key relationship to Question
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # Choice text
    choice_text = models.CharField(max_length=300)
    # Boolean indicator whether this choice is correct
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.choice_text} (Correct: {self.is_correct})"


# Submission Model
class Submission(models.Model):
    # Foreign key relationship to Course
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    # Optional foreign key to Enrollment (links to learner attempt)
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, null=True, blank=True)
    # Many-to-many relationship with Choice to store the submitted choices
    choices = models.ManyToManyField(Choice)
    time_submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission #{self.id} for {self.course.name} on {self.time_submitted.strftime('%Y-%m-%d %H:%M')}"
