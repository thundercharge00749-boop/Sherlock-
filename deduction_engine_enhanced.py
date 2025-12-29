
import json
from typing import List, Dict, Tuple

class DeductionEngine:
    def __init__(self):
        # --- LAYER 1: THE CUE DATABASE ---
        # Weighted cues based on forensic psychology and behavioral profiling.
        self.cue_library = {
            "PHYSICAL_MARKERS": {
                "inward_watch_face": {"Military": 9, "Medical": 7, "Tactical": 8},
                "tactical_nail_cut": {"Military": 7, "Security": 6, "Blue_Collar": 4},
                "callous_index_finger": {"Heavy_Tool_User": 8, "Tradesman": 7},
                "writer_bump_middle_finger": {"Academic": 8, "Journalist": 7, "Student": 5},
                "watch_tan_line_empty": {"Financial_Distress": 6, "Recent_Loss": 5},
                "pristine_shoes_scruffy_cuffs": {"Aspirational_Status": 8, "Social_Climber": 7},
                "nicotine_stains_fingers": {"High_Anxiety": 7, "Addiction_Prone": 8},
                "asymmetric_muscle_development": {"Specialized_Labor": 7, "Sports_Professional": 6},
                "teeth_grinding_wear": {"Chronic_Stress": 8, "Sleep_Disorder": 6},
                "bitten_nails": {"Anxiety_Disorder": 7, "Nervous_Habit": 8},
                "ink_stains_specific_fingers": {"Writer": 8, "Artist": 6, "Forger": 5},
                "calloused_knees": {"Religious_Practice": 7, "Manual_Labor": 5}
            },
            "BEHAVIORAL_CLUSTERS": {
                "peripheral_scanning": {"Hyper_Vigilance": 9, "Security_Training": 8},
                "ventral_shielding_low": {"Fear_Response": 8, "Lying": 6},
                "ventral_shielding_high": {"Defiance": 7, "Stubbornness": 8},
                "feet_pointing_exit": {"Desire_To_Escape": 10, "Disinterest": 9},
                "neck_pacifying_touch": {"High_Stress": 9, "Deception": 6},
                "micro_expression_contempt": {"Hostility": 10, "Relationship_Danger": 9},
                "lack_of_startle_response": {"Psychopathy": 8, "High_Training": 7},
                "hand_steepling": {"Confidence": 8, "Dominance": 7},
                "ankle_locking": {"Defensive_Posture": 7, "Withholding_Info": 8},
                "ventral_denial": {"Disagreement": 9, "Rejection": 8},
                "eye_blocking": {"Disbelief": 8, "Stress": 7},
                "lip_compression": {"Anger_Suppression": 9, "Disagreement": 8}
            },
            "MICRO_EXPRESSIONS": {
                # Based on FACS (Facial Action Coding System)
                "unilateral_lip_curl": {"Contempt": 10, "Superiority_Complex": 9},
                "flash_fear_eyes": {"Genuine_Fear": 9, "Trauma_Trigger": 8},
                "flash_disgust_nose": {"Moral_Disgust": 8, "Physical_Repulsion": 7},
                "asymmetric_smile": {"Fake_Happiness": 9, "Social_Masking": 8},
                "eyebrow_flash_surprise": {"Genuine_Surprise": 9, "Recognition": 7},
                "duchenne_smile": {"Genuine_Joy": 10, "Authentic_Pleasure": 9},
                "partial_shrug": {"Uncertainty": 7, "Deception": 8},
                "nose_wrinkle": {"Disgust": 9, "Aversion": 8},
                "chin_raise": {"Pride": 7, "Defiance": 8}
            },
            "FORENSIC_LINGUISTICS": {
                # Verbal deception indicators
                "past_tense_present_event": {"Deception": 10, "Distancing": 9},
                "excessive_detail_irrelevant": {"Overcompensation": 8, "Rehearsed_Story": 9},
                "pronoun_avoidance": {"Deception": 9, "Denial_Of_Involvement": 8},
                "verb_tense_inconsistency": {"Fabrication": 9, "Memory_Construction": 7},
                "spontaneous_corrections": {"Truth_Telling": 8, "Genuine_Memory": 7},
                "admission_lack_memory": {"Honesty": 9, "Authentic_Recall": 8},
                "unusual_word_choice": {"Deception": 7, "Scripted_Response": 8},
                "denial_before_accusation": {"Guilty_Conscience": 10, "Preemptive_Defense": 9},
                "non_contracted_denial": {"Formal_Lying": 9, "Emphatic_Deception": 8},
                "complaint_language": {"Deception": 6, "Deflection": 7},
                "negative_statement_excess": {"Deception": 7, "Emotional_Distress": 6},
                "minimal_self_reference": {"Deceptive_Distancing": 8, "Low_Commitment": 7},
                "shorter_response_length": {"Deception": 7, "Information_Withholding": 8},
                "answering_with_question": {"Stalling_Tactic": 8, "Evasion": 9},
                "temporal_sequencing_error": {"False_Memory": 8, "Fabrication": 9}
            },
            "VOCAL_MARKERS": {
                "voice_pitch_elevation": {"Stress": 8, "Deception": 7},
                "speech_rate_increase": {"Anxiety": 7, "Excitement": 6},
                "speech_rate_decrease": {"Careful_Fabrication": 8, "Depression": 6},
                "vocal_tremor": {"Fear": 9, "Emotional_Distress": 8},
                "speech_disfluency": {"Cognitive_Load": 8, "Deception": 7},
                "latency_increase": {"Fabrication": 8, "Cognitive_Processing": 6}
            },
            "DARK_TRIAD_MARKERS": {
                "love_bombing_speech": {"Narcissism": 9, "Manipulator": 8},
                "superficial_charm": {"Psychopathy": 7, "Narcissism": 8},
                "victim_signaling": {"Covert_Narcissism": 8, "Machiavellianism": 7},
                "lack_empathy_verbal": {"Psychopathy": 10, "Antisocial": 9},
                "grandiose_statements": {"Narcissism": 9, "Superiority_Complex": 8},
                "manipulation_language": {"Machiavellianism": 10, "Dark_Persuasion": 9},
                "blame_shifting": {"Narcissism": 8, "Accountability_Avoidance": 7}
            },
            "CONTEXT_FILTERS": {
                # Modifies weights based on environment
                "high_temperature": {"High_Stress": -5, "Fear_Response": -4, "Anxiety": -3},
                "formal_event": {"Military": 3, "High_Status": 2},
                "medical_setting": {"Medical": 5, "Anxiety": 4},
                "first_date": {"Anxiety": -3, "High_Stress": -2},
                "job_interview": {"Anxiety": -4, "High_Stress": -3},
                "court_setting": {"Anxiety": -3, "Deception": 2},
                "police_interrogation": {"High_Stress": -4, "Fear_Response": -3}
            }
        }

    # --- LAYER 2: THE CONFLICT DETECTOR ---
    def detect_incongruence(self, observed_cues: List[str]) -> List[str]:
        conflicts = []

        # Status incongruence
        if "expensive_watch" in observed_cues and "frayed_collar" in observed_cues:
            conflicts.append("STATUS INCONGRUENCE: Subject prioritizes public signaling over private maintenance.")

        # Emotional leakage
        if "calm_voice" in observed_cues and "shaking_hands" in observed_cues:
            conflicts.append("EMOTIONAL LEAKAGE: Subject is suppressing high adrenaline/rage.")

        if "asymmetric_smile" in observed_cues and "duchenne_smile" in observed_cues:
            conflicts.append("EMOTIONAL MASKING: Genuine and fake happiness signals detected simultaneously.")

        # Linguistic incongruence
        if "past_tense_present_event" in observed_cues and "spontaneous_corrections" in observed_cues:
            conflicts.append("LINGUISTIC PARADOX: Deceptive distancing co-exists with truth-telling markers.")

        # Behavioral contradiction
        if "hand_steepling" in observed_cues and "ankle_locking" in observed_cues:
            conflicts.append("CONFIDENCE-FEAR SPLIT: Displays dominance while body shows defensive retreat.")

        # Micro-expression vs macro behavior
        if "flash_fear_eyes" in observed_cues and "lack_of_startle_response" in observed_cues:
            conflicts.append("FEAR SUPPRESSION: Micro-fear detected but controlled startle response suggests training or psychopathy.")

        return conflicts

    # --- LAYER 3: THE ANALYSIS LOGIC ---
    def analyze(self, observed_cues: List[str], environmental_context: List[str]) -> Tuple[List[Dict], List[str]]:
        profiles = {}

        # 1. Base Weighting
        for category in ["PHYSICAL_MARKERS", "BEHAVIORAL_CLUSTERS", "MICRO_EXPRESSIONS", 
                        "FORENSIC_LINGUISTICS", "VOCAL_MARKERS", "DARK_TRIAD_MARKERS"]:
            for cue in observed_cues:
                if cue in self.cue_library.get(category, {}):
                    for profile, weight in self.cue_library[category][cue].items():
                        profiles[profile] = profiles.get(profile, 0) + weight

        # 2. Context Adjustment
        for context in environmental_context:
            if context in self.cue_library["CONTEXT_FILTERS"]:
                for profile, modifier in self.cue_library["CONTEXT_FILTERS"][context].items():
                    if profile in profiles:
                        profiles[profile] += modifier
                        # Ensure no negative scores
                        if profiles[profile] < 0:
                            profiles[profile] = 0

        # 3. Confidence Calculation & Sorting
        final_report = []
        sorted_profiles = sorted(profiles.items(), key=lambda x: x[1], reverse=True)

        for profile, score in sorted_profiles:
            if score <= 0:
                continue

            confidence = "Low"
            threat_level = "Normal"

            if score >= 20: 
                confidence = "Critical/Certain"
                threat_level = "Extreme"
            elif score >= 15: 
                confidence = "Very High"
                threat_level = "High"
            elif score >= 10: 
                confidence = "High"
                threat_level = "Moderate"
            elif score >= 6: 
                confidence = "Medium"
                threat_level = "Low"

            final_report.append({
                "Profile": profile,
                "Probability_Score": score,
                "Confidence": confidence,
                "Threat_Level": threat_level
            })

        return final_report, self.detect_incongruence(observed_cues)

    def get_all_cues_by_category(self) -> Dict[str, List[str]]:
        """Returns all available cues organized by category for UI population"""
        result = {}
        for category, cues in self.cue_library.items():
            if category != "CONTEXT_FILTERS":
                result[category] = list(cues.keys())
        return result

    def get_context_options(self) -> List[str]:
        """Returns all available context filters"""
        return list(self.cue_library["CONTEXT_FILTERS"].keys())
