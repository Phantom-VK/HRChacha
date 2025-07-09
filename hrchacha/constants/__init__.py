from dataclasses import dataclass
from typing import List
from pathlib import Path


USER_CHAT_INPUT_KEY = "ucik"
PROJECT_ROOT = Path(__file__).parent.parent.parent

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
        greeting = ("🤖 **Welcome to TalentScout AI Hiring Assistant!**\n\n"
    "Hello! I'm your AI-powered hiring assistant. I help with your initial screening for tech roles.\n\n"
    "**Here's what I’ll do:**\n"
    "\t✅ Collect your basic info\n"
    "\t✅ Understand your tech skills\n"
    "\t✅ Ask 3–5 relevant technical questions\n"
    "\t✅ Make your first screening quick and smooth\n\n"
    "**Conversation Flow:**\n"
    "\t1. Personal Info – Name, contact, experience\n"
    "\t2. Tech Background – Your stack & tools\n"
    "\t3. Tech Assessment – I’ll ask you questions\n"
    "\t4. Next Steps – What happens after this chat\n\n"
    "**Before We Start:**\n"
    "\t• This will take ~10–15 minutes\n"
    "\t• Please give accurate info for best results\n"
    "\t• Type 'exit', 'quit', or 'bye' anytime to stop\n\n"
    "**Privacy:**\n"
    "\t🔒 Your data is secure and encrypted\n"
    "\t🔒 We follow strict privacy standards\n"
    "\t🔒 Used only for recruitment purposes\n\n"
    "---\n"
    "Let’s get started! Please tell me your **full name** below.\n")
        return greeting

    @staticmethod
    def get_welcome_back_message(candidate_name=None):
        """
        Returns a personalized welcome back message for returning users
        """
        if candidate_name:
            return (
                f"🤖 **Welcome back, {candidate_name}!**\n\n"
                "I see we’ve chatted before.\n"
                "Would you like to:\n"
                "\t1. Continue from where we left off\n"
                "\t2. Start a fresh conversation\n"
                "\t3. Update your info\n\n"
                "Let me know how you'd like to proceed!"
            )
        else:
            return (
                "🤖 **Welcome back to TalentScout!**\n\n"
                "Looks like you’re returning to complete your profile.\n"
                "Let’s pick up where we left off!"
            )

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