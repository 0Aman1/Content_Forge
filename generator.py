"""Content generation engine using Groq API for cloud-hosted LLM inference"""

import os
from typing import Optional, List, Dict, Any
from groq import Groq
from prompts import PromptBuilder


class GroqManager:
    """Manage Groq API model connections and operations"""

    DEFAULT_MODEL = "gpt-oss-20b"

    # Maps user-facing model names to Groq-hosted model identifiers
    MODEL_MAP = {
        "gpt-oss-20b": "openai/gpt-oss-20b",
        "gpt-oss-120b": "openai/gpt-oss-120b",
        "qwen-27b": "qwen/qwen3.8-27b",
        "allam-7b": "allam-2-7b",
    }

    AVAILABLE_MODELS = list(MODEL_MAP.keys())

    def __init__(self, model: str = DEFAULT_MODEL):
        self.model = model
        self._client = None

    def _get_client(self) -> Groq:
        """Lazily initialise the Groq client using the environment variable."""
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise ValueError(
                "GROQ_API_KEY environment variable is not set. "
                "Please add your Groq API key to the environment or a .env file."
            )
        if self._client is None:
            self._client = Groq(api_key=api_key)
        return self._client

    @staticmethod
    def is_api_configured() -> bool:
        """Check if the Groq API key is available in the environment."""
        return bool(os.environ.get("GROQ_API_KEY"))

    @staticmethod
    def get_available_models() -> List[str]:
        """Return the list of user-facing model names."""
        return list(GroqManager.MODEL_MAP.keys())

    def _resolve_model(self, model_name: str | None = None) -> str:
        """Resolve a user-facing model name to its Groq identifier."""
        name = model_name or self.model
        return self.MODEL_MAP.get(name, name)

    def test_connection(self) -> bool:
        """Test connectivity to the Groq API with the current model."""
        try:
            client = self._get_client()
            response = client.chat.completions.create(
                model=self._resolve_model(),
                messages=[{"role": "user", "content": "Say 'OK' only"}],
                max_tokens=5,
                temperature=0,
            )
            text = response.choices[0].message.content.strip().upper()
            return "OK" in text
        except Exception:
            return False

    def set_model(self, model_name: str):
        """Set the model to use."""
        self.model = model_name

    def get_current_model(self) -> str:
        """Get current user-facing model name."""
        return self.model

    def get_groq_model_id(self) -> str:
        """Get the Groq model identifier for the current model."""
        return self._resolve_model()

    def get_status(self) -> Dict[str, Any]:
        """Return status information about the Groq configuration."""
        return {
            "model": self.model,
            "groq_model_id": self._resolve_model(),
            "api_configured": self.is_api_configured(),
            "status": (
                "🟢 Groq API key configured"
                if self.is_api_configured()
                else "🔴 GROQ_API_KEY not set"
            ),
        }


class ContentGenerator:
    """Generate content using the Groq API"""

    def __init__(self, groq_manager: GroqManager = None):
        if groq_manager is None:
            groq_manager = GroqManager()
        self.groq_manager = groq_manager
        self.timeout = 300  # 5 minutes timeout

    def _call_groq(self, prompt_text: str, temperature: float = 0.7) -> str:
        """Send a prompt to the Groq API and return the response text."""
        client = self.groq_manager._get_client()
        response = client.chat.completions.create(
            model=self.groq_manager._resolve_model(),
            messages=[{"role": "user", "content": prompt_text}],
            temperature=temperature,
        )
        return response.choices[0].message.content.strip()

    def generate_content(
        self,
        content_type: str,
        topic: str,
        audience: str,
        tone: str,
        style: str,
        length: str,
        language: str,
        keywords: str,
        creativity: float = 0.7,
        num_outputs: int = 1,
    ) -> List[str]:
        """Generate content based on parameters"""

        prompt_text = PromptBuilder.build_prompt(
            content_type=content_type,
            topic=topic,
            audience=audience,
            tone=tone,
            style=style,
            length=length,
            language=language,
            keywords=keywords,
            creativity=creativity,
        )

        outputs = []
        for i in range(num_outputs):
            try:
                response = self._call_groq(prompt_text, temperature=creativity)
                if response:
                    outputs.append(response)
            except Exception as e:
                raise ValueError(f"Error generating content: {str(e)}")

        return outputs if outputs else ["Error: No content generated. Please try again."]

    def rewrite_content(
        self, original_text: str, rewrite_type: str, tone: str = None, style: str = None
    ) -> str:
        """Rewrite existing content"""

        prompt_text = PromptBuilder.build_rewrite_prompt(
            original_text=original_text,
            rewrite_type=rewrite_type,
            tone=tone,
            style=style,
        )

        try:
            response = self._call_groq(prompt_text, temperature=0.5)
            return response if response else original_text
        except Exception as e:
            raise ValueError(f"Error rewriting content: {str(e)}")

    def enhance_content(self, original_text: str, enhancement_type: str) -> str:
        """Enhance existing content"""

        prompt_text = PromptBuilder.build_enhancement_prompt(
            original_text=original_text, enhancement_type=enhancement_type
        )

        try:
            response = self._call_groq(prompt_text, temperature=0.6)
            return response if response else original_text
        except Exception as e:
            raise ValueError(f"Error enhancing content: {str(e)}")

    def generate_from_template(
        self, template_text: str, placeholders: dict, creativity: float = 0.7
    ) -> str:
        """Generate content from template with placeholders"""

        filled_template = template_text
        for placeholder, value in placeholders.items():
            filled_template = filled_template.replace(f"{{{placeholder}}}", value)

        prompt_text = f"""Based on this template, generate complete content:

{filled_template}

Important: Generate ONLY the content, no explanations."""

        try:
            response = self._call_groq(prompt_text, temperature=creativity)
            return response if response else filled_template
        except Exception as e:
            raise ValueError(f"Error generating from template: {str(e)}")

    def batch_generate(
        self, prompts: List[str], temperature: float = 0.7
    ) -> List[str]:
        """Generate multiple outputs from multiple prompts"""

        outputs = []

        for prompt in prompts:
            try:
                response = self._call_groq(prompt, temperature=temperature)
                if response:
                    outputs.append(response)
            except Exception:
                outputs.append("")

        return outputs

    def get_model_info(self) -> dict:
        """Get information about current model"""
        status = self.groq_manager.get_status()
        return {
            "model": self.groq_manager.get_current_model(),
            "groq_model_id": self.groq_manager.get_groq_model_id(),
            "api_configured": self.groq_manager.is_api_configured(),
            "available_models": self.groq_manager.get_available_models(),
            "status": status,
        }
