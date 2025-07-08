from dataclasses import dataclass
from typing import List

USER_CHAT_INPUT_KEY = "ucik"


class ConversationState:
    GREETING = "greeting"
    COLLECTING_INFO = "collecting_info"
    TECH_STACK = "tech_stack"
    TECHNICAL_QUESTIONS = "technical_questions"
    RECOMMENDER = "recommender"
    CONCLUSION = "conclusion"


@dataclass
class User:
    name:str = ""
    email:str = ""
    phone:str = ""
    experience:str = ""
    desired_positions: str | List[str] = ""
    tech_stack: List[str] = ""
    curr_location:str = ""

@dataclass
class Job:
    name:str
    required_expr:str
    contact:str
    description:str
    requirements: str
    location: List[str]
    salary:str


class GreetingMessage:
    """
    Handles the initial greeting and introduction for the hiring assistant chatbot
    """

    @staticmethod
    def get_main_greeting() -> str:
        """
        Returns the main greeting message displayed when chatbot starts
        """
        greeting = """
🤖 **Welcome to TalentScout AI Hiring Assistant!**

Hello! I'm your AI-powered hiring assistant, here to help streamline your initial interview process. I specialize in technology placements and I'm excited to learn about your background and skills.

**What I'll Help You With:**
✅ Collect your professional information
✅ Understand your technical expertise
✅ Ask relevant technical questions based on your skills
✅ Ensure a smooth initial screening process

**Here's How Our Conversation Will Flow:**
1. **Personal Information** - I'll gather your basic details (name, contact, experience)
2. **Technical Background** - You'll share your tech stack and expertise areas
3. **Technical Assessment** - I'll ask 3-5 relevant technical questions
4. **Next Steps** - I'll explain what happens after our conversation

**What You Need to Know:**
• This conversation typically takes 10-15 minutes
• Please provide accurate information for the best experience
• All your data is handled securely and professionally
• You can type 'exit', 'quit', or 'bye' anytime to end our chat

**Privacy & Security:**
🔒 Your information is encrypted and stored securely
🔒 We follow strict data privacy standards
🔒 Your details will only be used for recruitment purposes

---

Let's get started! Could you please tell me your **full name**?

*Type your response below and I'll guide you through the rest of the process.*
        """
        return greeting.strip()

    @staticmethod
    def get_welcome_back_message(candidate_name=None):
        """
        Returns a personalized welcome back message for returning users
        """
        if candidate_name:
            return f"""
🤖 **Welcome back, {candidate_name}!**

I see we've chatted before. Would you like to:
1. Continue from where we left off
2. Start a fresh conversation
3. Update your information

Please let me know how you'd like to proceed!
            """
        else:
            return """
🤖 **Welcome back to TalentScout!**

I see you've returned to complete your profile. Let's pick up where we left off.
            """

    @staticmethod
    def get_after_hours_greeting():
        """
        Returns a greeting message for after-hours interactions
        """
        return """
🤖 **Welcome to TalentScout AI Hiring Assistant!**

Thank you for your interest in joining our talent pool! While our human recruiters are currently offline, I'm here 24/7 to help you get started with your initial screening.

I'll collect your information and technical background, so our recruitment team can review your profile first thing tomorrow morning.

Let's begin! Could you please tell me your **full name**?
        """

    @staticmethod
    def get_technical_transition_message():
        """
        Message shown when transitioning from info collection to technical questions
        """
        return """
📋 **Great! I've collected your basic information.**

Now let's dive into the technical part. Based on your expertise, I'll ask you a few relevant questions to assess your skills.

**What to Expect:**
• 3-5 technical questions tailored to your tech stack
• Questions will cover practical scenarios and concepts
• Take your time to provide thoughtful answers
• There are no trick questions - just showcase your knowledge

Ready to begin the technical assessment? Let's start with your first question!
        """

    @staticmethod
    def get_conclusion_message(candidate_name):
        """
        Final message shown at the end of the conversation
        """
        return f"""
🎉 **Thank you, {candidate_name}!**

You've successfully completed the initial screening with TalentScout AI Hiring Assistant.

**What Happens Next:**
1. **Review Process** - Our recruitment team will review your profile within 24-48 hours
2. **Technical Assessment** - Your answers will be evaluated by our technical experts
3. **Next Steps** - If there's a good match, we'll contact you for the next round
4. **Communication** - We'll keep you updated via email about your application status

**Contact Information:**
📧 Email: careers@talentscout.com
📞 Phone: +91-XXX-XXX-XXXX
🌐 Website: www.talentscout.com

**Important Notes:**
• Keep an eye on your email (including spam folder) for updates
• Feel free to reach out if you have any questions
• We appreciate your time and interest in working with us

**Thank you for choosing TalentScout for your career journey!**

Have a great day! 😊

*This conversation has been saved securely. You can close this window now.*
        """

    @staticmethod
    def get_error_recovery_message():
        """
        Message shown when chatbot encounters an error and needs to restart
        """
        return """
🤖 **Oops! Something went wrong.**

I apologize for the technical difficulty. Let me restart our conversation to ensure you have the best experience.

Don't worry - I'll make sure we get you through the screening process smoothly.

Let's start fresh! Could you please tell me your **full name**?
        """

    @staticmethod
    def get_session_timeout_message():
        """
        Message shown when session times out
        """
        return """
⏰ **Session Timeout Notice**

Your session has been inactive for a while. For security reasons, I'll need to restart our conversation.

No worries - this is just a precautionary measure to protect your information.

Let's begin again! Could you please tell me your **full name**?
        """