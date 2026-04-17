from collections import defaultdict, Counter
import statistics
import math

# -----------------------------
# CONFIG
# -----------------------------
STYLES = ["Activist", "Reflector", "Theorist", "Pragmatist"]

MCQ_WEIGHT = 0.4
TASK_WEIGHT = 0.6

# -----------------------------
# ENGINE
# -----------------------------
class MPrintEngine:

    def __init__(self):
        self.mcq_scores = defaultdict(float)
        self.task_scores = defaultdict(float)
        self.response_log = []

    # -----------------------------
    # ADD RESPONSE
    # -----------------------------
    def add_response(self, style, q_type="mcq", weight=1, time_taken=None):
        if style not in STYLES:
            return

        if q_type == "mcq":
            self.mcq_scores[style] += weight
        elif q_type == "task":
            self.task_scores[style] += weight

        self.response_log.append({
            "style": style,
            "type": q_type,
            "time": time_taken
        })

    # -----------------------------
    # WEIGHTED SCORES
    # -----------------------------
    def compute_weighted_scores(self):
        return {
            style: (self.mcq_scores[style] * MCQ_WEIGHT +
                    self.task_scores[style] * TASK_WEIGHT)
            for style in STYLES
        }

    # -----------------------------
    # NORMALIZE
    # -----------------------------
    def normalize(self, scores):
        total = sum(scores.values())
        if total == 0:
            return {k: 0 for k in scores}
        return {k: round((v / total) * 100, 2) for k, v in scores.items()}

    # -----------------------------
    # CONFIDENCE
    # -----------------------------
    def confidence_score(self, normalized):
        vals = sorted(normalized.values(), reverse=True)

        if len(vals) < 2:
            return 0

        top = vals[0]
        second = vals[1]

        # difference-based confidence (scaled properly)
        confidence = (top - second)

        # already percentage range, just cap
        return round(min(confidence, 100), 2)

    # -----------------------------
    # CONSISTENCY
    # -----------------------------
    def consistency_score(self):
        styles = [r["style"] for r in self.response_log]
        if not styles:
            return 0
        most_common = Counter(styles).most_common(1)[0][1]
        return round(most_common / len(styles), 2)

    # -----------------------------
    # ENTROPY
    # -----------------------------
    def entropy_score(self, normalized):
        probs = [v / 100 for v in normalized.values() if v > 0]
        return round(-sum(p * math.log(p, 2) for p in probs), 3)

    # -----------------------------
    # SPEED BIAS (Z-score)
    # -----------------------------
    def speed_bias(self):
        times = [r["time"] for r in self.response_log if r["time"] is not None]

        if len(times) < 3:
            return None

        mean = statistics.mean(times)
        std = statistics.stdev(times)

        if std == 0:
            return None

        fast_styles = []
        for r in self.response_log:
            if r["time"] is None:
                continue

            z = (r["time"] - mean) / std

            if z < -0.5:  # faster than personal avg
                fast_styles.append(r["style"])

        if not fast_styles:
            return None

        return Counter(fast_styles).most_common(1)[0][0]

    # -----------------------------
    # FIRST CHOICE
    # -----------------------------
    def first_choice_bias(self):
        if not self.response_log:
            return None
        return self.response_log[0]["style"]

    # -----------------------------
    # DYNAMIC BIAS PENALTY
    # -----------------------------
    def dynamic_bias_penalty(self, normalized):
        styles = [r["style"] for r in self.response_log]
        counts = Counter(styles)

        dominant, freq = counts.most_common(1)[0]
        total = len(styles)

        dominance_ratio = freq / total
        entropy = self.entropy_score(normalized)
        consistency = self.consistency_score()

        # Normalize entropy (max ~2 for 4 classes)
        entropy_factor = 1 - (entropy / 2)
        consistency_factor = consistency

        bias_intensity = (
            dominance_ratio * 0.5 +
            entropy_factor * 0.3 +
            consistency_factor * 0.2
        )

        bias_intensity = min(max(bias_intensity, 0), 1)

        # penalty range: 0.7 → 1.0
        penalty = 1 - (0.3 * bias_intensity)

        return dominant, penalty, bias_intensity

    # -----------------------------
    # APPLY BIAS
    # -----------------------------
    def adjust_for_bias(self, normalized):
        dominant, penalty, intensity = self.dynamic_bias_penalty(normalized)

        if intensity > 0.6:
            normalized[dominant] *= penalty
            bias_flag = True
        else:
            bias_flag = False

        return normalized, bias_flag, dominant, intensity, penalty

    # -----------------------------
    # FINAL ENGINE
    # -----------------------------
    def generate_mprint(self):

        # Step 1: Weighted scores
        weighted = self.compute_weighted_scores()

        # Step 2: Normalize
        normalized = self.normalize(weighted)

        # Step 3: Bias adjust
        normalized, bias_flag, bias_style, intensity, penalty = self.adjust_for_bias(normalized)

        # Step 4: Re-normalize
        normalized = self.normalize(normalized)

        # Step 5: Metrics
        confidence = self.confidence_score(normalized)
        consistency = self.consistency_score()
        entropy = self.entropy_score(normalized)

        # Step 6: Ranking
        sorted_styles = sorted(normalized.items(), key=lambda x: x[1], reverse=True)
        top1, top2 = sorted_styles[0], sorted_styles[1]

        # -----------------------------
        # TIE-BREAKER
        # -----------------------------
        if top1[1] == top2[1]:

            # Layer 1: Task dominance
            task_sorted = sorted(self.task_scores.items(), key=lambda x: x[1], reverse=True)
            if len(task_sorted) > 1 and task_sorted[0][1] != task_sorted[1][1]:
                dominant = task_sorted[0][0]
            else:
                # Layer 2: First choice
                dominant = self.first_choice_bias()

                # Layer 3: Speed bias
                if not dominant:
                    dominant = self.speed_bias()

                # Fallback
                if not dominant:
                    dominant = top1[0]
        else:
            dominant = top1[0]

        # -----------------------------
        # HYBRID PROFILE
        # -----------------------------
        if confidence < 10:
            profile = f"{top1[0]}-{top2[0]}"
        else:
            profile = top1[0]

        return {
            "dominant_style": dominant,
            "profile": profile,
            "distribution": normalized,
            "confidence": confidence,
            "consistency": consistency,
            "entropy": entropy,
            "bias_flag": bias_flag,
            "bias_style": bias_style,
            "bias_intensity": round(intensity, 3),
            "penalty_applied": round(penalty, 3) if bias_flag else 1.0,
            "note": "Possible response bias detected" if bias_flag else "Profile computed successfully"
        }


# -----------------------------
# EXAMPLE RUN
# -----------------------------
if __name__ == "__main__":

    engine = MPrintEngine()

    # Simulated responses
    engine.add_response("Activist", "mcq", 2, 2)
    engine.add_response("Activist", "task", 2, 1)
    engine.add_response("Activist", "mcq", 2, 2)
    engine.add_response("Reflector", "mcq", 2, 5)
    engine.add_response("Theorist", "task", 2, 6)
    engine.add_response("Activist", "task", 2, 1)
    engine.add_response("Activist", "mcq", 2, 2)

    result = engine.generate_mprint()

    print(result)
