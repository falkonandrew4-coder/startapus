# Програмний продукт розроблено Соколом Андрієм - Falkon AI

class ProjectStateMachine:
    """
    Керує логікою 4 етапів проекту: 
    Штурм -> Аналіз ринку -> 20 питань -> Генерація ТЗ
    """
    
    STAGES = [
        "brainstorming",
        "market_analysis",
        "deep_questions",
        "artifact_generation",
        "completed"
    ]

    @staticmethod
    def get_next_stage(current_stage: str) -> str:
        try:
            index = ProjectStateMachine.STAGES.index(current_stage)
            if index + 1 < len(ProjectStateMachine.STAGES):
                return ProjectStateMachine.STAGES[index + 1]
            return "completed"
        except ValueError:
            return "brainstorming"

    @staticmethod
    def get_system_prompt_for_stage(stage: str) -> str:
        # Тут ми будемо підтягувати промпти з бази Supabase
        if stage == "brainstorming":
            return "Ти допомагаєш генерувати ідеї..."
        elif stage == "market_analysis":
            return "Ти аналізуєш результати пошуку з DuckDuckGo..."
        elif stage == "deep_questions":
            return "Задай 4 питання користувачу..."
        elif stage == "artifact_generation":
            return "Згенеруй фінальне ТЗ та Vibe-Coding промпт..."
        return ""
