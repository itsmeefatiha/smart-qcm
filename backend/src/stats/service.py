from .repository import StatsRepository

class StatsService:
    @staticmethod
    def get_global_stats():
        """Overview for the Manager Dashboard"""
        # 1. Fetch data from Repository
        total_students = StatsRepository.count_users_by_role("student")
        total_exams = StatsRepository.count_total_exams()
        total_attempts = StatsRepository.count_total_attempts()
        avg_score = StatsRepository.get_global_average_score()
        
        # 2. Return formatted dictionary
        return {
            "total_students": total_students,
            "total_exams": total_exams,
            "total_attempts": total_attempts,
            "average_score": round(avg_score, 2)
        }

    @staticmethod
    def get_branch_performance(branch_id):
        """Pass/Fail rates for a specific branch"""
        # 1. Fetch raw attempts
        attempts = StatsRepository.get_attempts_by_branch(branch_id)
        
        if not attempts:
            return {"message": "No data for this branch", "attempts": 0}

        # 2. Perform Logic / Calculations
        passed = 0
        failed = 0
        total_score = 0
        
        for attempt in attempts:
            total_score += attempt.score
            
            # Logic: Passing grade is 50% of total
            # (You could make this configurable later)
            passing_grade = attempt.session.total_grade / 2
            
            if attempt.score >= passing_grade:
                passed += 1
            else:
                failed += 1
                
        # 3. Final Formatting
        return {
            "attempts": len(attempts),
            "passed": passed,
            "failed": failed,
            "success_rate": round((passed / len(attempts)) * 100, 1),
            "avg_grade": round(total_score / len(attempts), 2)
        }
    
    @staticmethod
    def get_hardest_questions_chart():
        """
        Returns data for a Horizontal Bar Chart.
        Shows the 'Failure Rate' (Percentage) of the top 5 hardest questions.
        """
        raw_data = StatsRepository.get_hardest_questions()
        
        labels = []
        data = []
        
        for q_text, total, wrong in raw_data:
            if total == 0: continue
            
            # Truncate long question text for the chart label
            short_text = (q_text[:40] + '..') if len(q_text) > 40 else q_text
            failure_rate = round((wrong / total) * 100, 1)
            
            labels.append(short_text)
            data.append(failure_rate)
            
        return {
            "labels": labels,
            "data": data,
            "label": "Failure Rate (%)" # Useful for Chart Legend
        }

    @staticmethod
    def get_completion_rate_chart():
        """
        Returns data for a Pie Chart: [Submitted, Abandoned]
        """
        total, finished = StatsRepository.get_completion_stats()
        
        abandoned = total - finished
        
        return {
            "labels": ["Submitted Successfully", "Abandoned / In Progress"],
            "data": [finished, abandoned]
        }