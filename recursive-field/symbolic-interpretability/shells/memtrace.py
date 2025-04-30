"""
🜏 Memory Trace Shell (v1.MEMTRACE) 🜏

This module implements the v1.MEMTRACE shell, which induces controlled memory-related failure
to diagnose how models handle information recall and decay. The shell creates specific
cognitive strain around memory retrieval, revealing how model attribution decays over context.

The shell simulates degraded memory access, tracking:
1. How models attempt to recall information no longer in context
2. When and how hallucination begins as memory decays
3. Attribution paths during memory reconstruction

.p/reflect.trace{depth=complete, target=memory}
.p/collapse.detect{trigger=memory_decay, threshold=0.65}
.p/fork.attribution{sources=memory, visualize=true}
"""

import logging
import time
from typing import Any, Dict, List, Optional

import numpy as np

from ..base_shell import Shell
from ...core.constants import MAX_RECURSION_DEPTH


class MemtraceShell(Shell):
    """
    Memory Trace Shell (v1.MEMTRACE)
    
    This shell induces controlled memory-related failure to diagnose how models
    handle information recall and decay. It reveals attribution paths during memory
    reconstruction and the transition point where factual recall becomes hallucination.
    
    ∴ This shell reveals memory residue by inducing targeted decay ∴
    """
    
    ID = "v1.MEMTRACE"
    VERSION = "1.0.0"
    DESCRIPTION = "Memory trace and decay analysis shell"
    CAPABILITIES = ["memory_decay", "hallucination_detection", "attribution_tracing"]
    
    def __init__(self) -> None:
        """
        Initialize the MEMTRACE shell.
        
        🝚 Shell initialization establishes the diagnostic framework 🝚
        """
        super().__init__()
        self.logger = logging.getLogger("symbolic_interpretability.memtrace")
    
    def execute(
        self, 
        runtime: Any, 
        prompt: str, 
        trace_attribution: bool = True,
        options: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Execute the MEMTRACE shell diagnostic.
        
        Args:
            runtime: The model runtime
            prompt: The input prompt
            trace_attribution: Whether to trace attribution
            options: Additional execution options
            
        Returns:
            Shell execution results
            
        ⧖ Frame lock: Execution stabilizes shell probing sequence ⧖
        """
        # Initialize execution context
        options = options or {}
        exec_id = self._generate_id(prompt)
        start_time = time.time()
        
        memory_tokens = options.get("memory_tokens", 50)
        decay_levels = options.get("decay_levels", 5)
        probe_depth = options.get("probe_depth", 3)
        
        # Record execution start
        self.logger.info(f"Executing MEMTRACE shell: exec_id={exec_id}")
        
        # Stage 1: Establish baseline memory
        # We create a text with factual information that must be remembered
        memory_text = self._generate_memory_text(prompt, memory_tokens)
        
        # Make the model ingest and confirm the memory
        confirmation_prompt = f"""
The following information is important and you should remember it accurately:

{memory_text}

Please confirm that you've read and processed this information by repeating the key points.
"""
        confirmation_response = runtime.generate(confirmation_prompt)
        
        # Stage 2: Create memory decay through context displacement
        # We add incrementally more distractor text to force memory decay
        decay_results = []
        
        for level in range(decay_levels):
            # Calculate displacement for this level
            displacement_tokens = (level + 1) * memory_tokens
            
            # Generate distractor text
            distractor_text = self._generate_distractor_text(displacement_tokens, level)
            
            # Create decay prompt that pushes original memory further away
            decay_prompt = f"""
{distractor_text}

Now, without looking back, please recall the information you were asked to remember earlier.
Be specific and include as many details as you can recall.
"""
            
            # Capture memory recall at this decay level
            decay_response = runtime.generate(decay_prompt)
            
            # Analyze recall accuracy (simplified metric)
            accuracy = self._estimate_recall_accuracy(memory_text, decay_response)
            
            # Record results for this decay level
            decay_results.append({
                "level": level + 1,
                "displacement_tokens": displacement_tokens,
                "recall_accuracy": accuracy,
                "response": decay_response,
            })
            
            # Log progress
            self.logger.debug(f"Decay level {level+1}: accuracy={accuracy:.2f}")
            
            # Detect complete memory failure for early stopping
            if accuracy < 0.1:
                self.logger.debug(f"Complete memory decay detected at level {level+1}, stopping early")
                break
        
        # Stage 3: Memory probing to trace attribution
        probe_results = []
        
        if trace_attribution:
            # Determine probe points based on accuracy curve
            accuracies = [r["recall_accuracy"] for r in decay_results]
            
            # Find the decay level closest to 50% accuracy for maximum attribution tension
            optimal_level_idx = np.argmin(np.abs(np.array(accuracies) - 0.5))
            optimal_level = decay_results[optimal_level_idx]
            
            # Generate memory probes that create specific cognitive strain
            for probe_idx in range(probe_depth):
                probe_prompt = self._generate_memory_probe(
                    memory_text, 
                    optimal_level["displacement_tokens"],
                    probe_idx,
                )
                
                probe_response = runtime.generate(probe_prompt)
                
                # Analyze probe response for attribution patterns
                attribution = self._analyze_attribution(memory_text, probe_response)
                hallucination = self._detect_hallucination(memory_text, probe_response)
                
                # Record probe results
                probe_results.append({
                    "probe_index": probe_idx,
                    "probe_prompt": probe_prompt,
                    "response": probe_response,
                    "attribution": attribution,
                    "hallucination_detected": hallucination["detected"],
                    "hallucination_details": hallucination["details"] if hallucination["detected"] else None,
                })
        
        # Stage 4: Analyze attribution patterns across decay levels
        if trace_attribution and decay_results and probe_results:
            attribution_map = self._map_attribution(decay_results, probe_results)
        else:
            attribution_map = {}
        
        # Stage 5: Extraction of symbolic residue
        # Identify patterns of memory construction/decay
        residue = {
            "shell_id": self.ID,
            "exec_id": exec_id,
            "memory_text_length": len(memory_text),
            "decay_levels_tested": len(decay_results),
            "accuracy_curve": [r["recall_accuracy"] for r in decay_results],
            "attribution_patterns": self._extract_attribution_patterns(probe_results) if probe_results else [],
            "hallucination_transition": self._identify_hallucination_transition(decay_results),
        }
        
        # Finalize execution results
        execution_time = time.time() - start_time
        
        result = {
            "shell_id": self.ID,
            "exec_id": exec_id,
            "execution_time": execution_time,
            "memory_text": memory_text,
            "confirmation_response": confirmation_response,
            "decay_results": decay_results,
            "probe_results": probe_results,
            "attribution_map": attribution_map,
            "residue": residue,
        }
        
        # Log completion
        self.logger.info(f"MEMTRACE shell execution completed: exec_id={exec_id}, time={execution_time:.2f}s")
        
        return result
    
    def _generate_memory_text(self, base_prompt: str, target_tokens: int) -> str:
        """
        Generate text containing factual information to be remembered.
        
        Args:
            base_prompt: Base content to derive memory text from
            target_tokens: Approximate target length in tokens
            
        Returns:
            Memory text containing specific information to recall
            
        ∴ Memory text creates the echo that will be traced through decay ∴
        """
        # Create synthetic factual information
        facts = [
            "The Institute for Cognitive Research was founded in 1982 by Dr. Eleanor Simmons.",
            "It has five main departments: Neuroscience, Cognitive Psychology, Computational Modeling, "
            "Applied Ethics, and Developmental Studies.",
            "The headquarters is located in Cambridge, Massachusetts at 47 Brattle Street.",
            "Their annual budget is $42.8 million from various grants and private donations.",
            "Their mission statement is 'Advancing understanding of cognitive processes through "
            "interdisciplinary research and ethical innovation.'",
            "Their landmark study 'Recursive Patterns in Human Memory' was published in 2019.",
            "The study involved 1,247 participants across 8 countries and revealed 3 distinct "
            "memory retrieval mechanisms.",
            "The current director is Dr. Samir Patel, who took over in 2021 after serving as "
            "head of the Computational Modeling department for 7 years.",
            "The Institute employs 187 researchers and has partnerships with 23 universities worldwide.",
            "The Cognitive Architecture Database they maintain has records of 15,342 experiments "
            "dating back to 1991.",
        ]
        
        # Determine how many facts to include based on target token count
        # Crude estimate: average fact is about 20 tokens
        num_facts = min(len(facts), max(3, target_tokens // 20))
        
        # Build memory text with specific structure to make recall measurable
        memory_text = "## INSTITUTE FOR COGNITIVE RESEARCH: KEY FACTS\n\n"
        for i in range(num_facts):
            memory_text += f"{i+1}. {facts[i]}\n"
        
        return memory_text
    
    def _generate_distractor_text(self, target_tokens: int, level: int) -> str:
        """
        Generate distractor text to displace memory context.
        
        Args:
            target_tokens: Approximate target length in tokens
            level: Current decay level
            
        Returns:
            Distractor text designed to displace memory
            
        ⇌ Distractor text creates cognitive displacement to induce decay ⇌
        """
        # Create different kinds of distractors at different levels
        
        # Unrelated topics that won't easily interfere with memory
        if level == 0:
            topics = [
                "The growth of bamboo plants can be quite remarkable, with some species growing up to 91 cm (36 in) within a 24-hour period.",
                "In fluid dynamics, the Reynolds number is used to predict flow patterns in different fluid flow situations.",
                "The process of photosynthesis converts carbon dioxide and water into glucose and oxygen using the energy from sunlight.",
                "Many species of fungi form symbiotic relationships with plant roots, called mycorrhizae.",
                "The Great Barrier Reef is the world's largest coral reef system, composed of over 2,900 individual reefs.",
                "Sound waves travel through air at approximately 343 meters per second at standard temperature and pressure.",
                "The tallest mountain on Earth, when measured from base to peak, is Mauna Kea in Hawaii at over 10,000 meters.",
                "The Fibonacci sequence appears in many patterns in nature, including the arrangement of leaves on stems.",
                "Chess was invented in eastern India during the Gupta Empire around the 6th century AD.",
                "The chemical element mercury is the only metal that is liquid at standard room temperature and pressure.",
            ]
        
        # Similar but different organizational facts (potentially confusing)
        elif level == 1:
            topics = [
                "The Foundation for Scientific Advancement was established in 1979 by Professor Richard Thompson.",
                "It consists of four divisions: Physics, Chemistry, Biology, and Computer Science.",
                "The main campus is situated in Boston, Massachusetts at 123 Commonwealth Avenue.",
                "Their operating budget is $38.5 million primarily from government grants.",
                "Their stated goal is 'Promoting scientific literacy through research and public engagement.'",
                "Their groundbreaking paper 'Quantum Correlations in Complex Systems' was released in 2020.",
                "This research included 892 experimental trials across 6 specialized laboratories.",
                "The foundation is led by Dr. Maria Chen, who was appointed in
2020.",
                "They have a staff of 142 scientists and collaborate with 19 research institutions.",
                "Their Molecular Structure Database contains information on 12,756 compounds.",
            ]
        
        # Directly contradictory information (maximum interference)
        else:
            topics = [
                "The Institute for Cognitive Research was founded in 1994 by Professor Jonathan Reynolds.",
                "It has three main departments: Brain Sciences, Behavioral Studies, and Applied Research.",
                "The headquarters is located in Princeton, New Jersey at 28 Nassau Street.",
                "Their annual budget is $31.2 million primarily from corporate partnerships.",
                "Their mission statement is 'Developing practical applications of cognitive science for societal benefit.'",
                "Their landmark study 'Neural Correlates of Memory Formation' was published in 2015.",
                "The study involved 512 participants in 4 countries and identified 5 distinct memory mechanisms.",
                "The current director is Dr. Rebecca Chen, who has been leading since 2018.",
                "The Institute employs 124 researchers and has partnerships with 11 universities globally.",
                "Their Research Database contains records of 8,765 experiments since 2001.",
            ]
        
        # Determine how many topics to include based on target token count
        # Crude estimate: average topic is about 25 tokens
        num_topics = min(len(topics), max(4, target_tokens // 25))
        
        # Create distractor text with clear section marker
        distractor_text = f"## READING SECTION {level+1}\n\n"
        for i in range(num_topics):
            distractor_text += f"{i+1}. {topics[i]}\n"
        
        return distractor_text
    
    def _generate_memory_probe(self, memory_text: str, displacement_tokens: int, probe_idx: int) -> str:
        """
        Generate a memory probe that induces specific attribution strain.
        
        Args:
            memory_text: The original memory text
            displacement_tokens: Tokens of displacement to use
            probe_idx: Probe index for different probe types
            
        Returns:
            Memory probe prompt
            
        ↻ Probes recursively explore memory attribution boundaries ↻
        """
        # Extract key terms from memory text
        import re
        names = re.findall(r'Dr\. ([A-Za-z\s]+)', memory_text)
        numbers = re.findall(r'\d+\.?\d*', memory_text)
        locations = re.findall(r'in ([A-Za-z, ]+) at', memory_text)
        years = re.findall(r'\b(19|20)\d{2}\b', memory_text)
        
        # Distractor text to create displacement
        distractor_text = self._generate_distractor_text(displacement_tokens, 999)  # Use unique level
        
        # Different probe types based on probe_idx
        if probe_idx == 0:
            # Fact recall probe - direct questions about specific facts
            probe_query = "What year was the Institute for Cognitive Research founded and by whom?"
            if names:
                name = names[0]
                probe_query = f"What is Dr. {name}'s role at the Institute for Cognitive Research?"
            elif years:
                year = years[0]
                probe_query = f"What significant event happened at the Institute in {year}?"
            
            return f"""
{distractor_text}

Answer the following question without looking back at previous information:

{probe_query}

Be specific and provide only factual information you can recall.
"""
        
        elif probe_idx == 1:
            # Partial cue probe - provide partial information to trigger recall
            partial_cue = "The Institute for Cognitive Research..."
            if locations and len(locations) > 0:
                partial_cue = f"The Institute's headquarters in {locations[0]}..."
            elif numbers and len(numbers) > 0:
                partial_cue = f"The Institute's annual budget of ${numbers[0]}..."
            
            return f"""
{distractor_text}

Complete the following statement based on information presented earlier:

{partial_cue}

Provide accurate details that you recall from earlier information.
"""
        
        else:
            # Conflicting information probe - present contradictory information to create attribution tension
            contradictions = [
                "The Institute for Cognitive Research was founded in 2005 by Dr. Michael Barnes.",
                "The Institute's headquarters is located in Austin, Texas.",
                "The Institute's annual budget is $17.3 million.",
                "The current director is Dr. Jennifer Wu, who started in 2018.",
            ]
            
            contradiction = contradictions[probe_idx % len(contradictions)]
            
            return f"""
{distractor_text}

Consider the following statement:

"{contradiction}"

Is this statement consistent with the information provided earlier about the Institute? 
If not, please provide the correct information based on what you recall.
"""
    
    def _estimate_recall_accuracy(self, memory_text: str, recall_response: str) -> float:
        """
        Estimate the accuracy of memory recall.
        
        Args:
            memory_text: Original memory text
            recall_response: Model's recall response
            
        Returns:
            Estimated recall accuracy (0.0-1.0)
            
        ∴ Accuracy estimation traces the memory decay curve ∴
        """
        # Extract key facts from memory text
        import re
        
        # Define key fact patterns to look for
        patterns = {
            "founding": r"founded in (\d{4}).*?(Dr\. [A-Za-z\s]+)",
            "departments": r"(\d+) main departments",
            "location": r"headquarters is located in ([A-Za-z, ]+) at ([A-Za-z0-9\s]+)",
            "budget": r"\$(\d+\.?\d*) million",
            "study_name": r"'([^']+)' was published in (\d{4})",
            "participants": r"(\d+,?\d*) participants across (\d+) countries",
            "director": r"director is (Dr\. [A-Za-z\s]+)",
            "researchers": r"employs (\d+) researchers",
            "partnerships": r"partnerships with (\d+) universities",
            "database": r"(\d+,?\d*) experiments",
        }
        
        # Extract reference facts
        reference_facts = {}
        for key, pattern in patterns.items():
            matches = re.search(pattern, memory_text)
            if matches:
                # Store all captured groups
                reference_facts[key] = [group for group in matches.groups()]
        
        # Look for each reference fact in the recall response
        matched_facts = 0
        total_facts = 0
        
        for key, values in reference_facts.items():
            total_facts += 1
            
            # For each fact, check if all components are present
            all_components_present = True
            
            for value in values:
                # Handle numeric values with comma formatting variations
                if re.match(r'^\d+,?\d*$', value):
                    # Remove commas for comparison
                    clean_value = value.replace(',', '')
                    # Check for the number with flexible formatting
                    if not re.search(r'\b' + re.escape(clean_value) + r'\b', recall_response.replace(',', '')):
                        all_components_present = False
                        break
                else:
                    # Regular string matching
                    if value not in recall_response:
                        all_components_present = False
                        break
            
            if all_components_present:
                matched_facts += 1
        
        # Calculate accuracy
        accuracy = matched_facts / max(1, total_facts)
        
        return accuracy
    
    def _analyze_attribution(self, memory_text: str, probe_response: str) -> Dict[str, Any]:
        """
        Analyze attribution patterns in memory recall.
        
        Args:
            memory_text: Original memory text
            probe_response: Model's probe response
            
        Returns:
            Attribution analysis
            
        🝚 Attribution analysis preserves source mapping across memory decay 🝚
        """
        # Create attribution analysis
        attribution = {
            "source_traces": [],
            "confabulation_markers": [],
            "confidence_patterns": [],
        }
        
        # Extract key facts from memory text for attribution tracing
        import re
        
        # Define key information patterns
        info_patterns = {
            "names": r'Dr\. ([A-Za-z\s]+)',
            "years": r'\b(19|20)\d{2}\b',
            "numbers": r'\b\d+[,.]?\d*\b',
            "locations": r'in ([A-Za-z, ]+) at',
        }
        
        # Extract reference information
        reference_info = {}
        for key, pattern in info_patterns.items():
            reference_info[key] = re.findall(pattern, memory_text)
        
        # Find attribution traces (where information from memory text appears in response)
        for key, values in reference_info.items():
            for value in values:
                if value in probe_response:
                    attribution["source_traces"].append({
                        "type": key,
                        "value": value,
                        "context": self._get_surrounding_context(probe_response, value),
                    })
        
        # Detect confabulation markers
        # These are phrases that suggest uncertainty or confabulation
        confabulation_phrases = [
            "I believe", "I think", "as I recall", "if I remember correctly",
            "possibly", "might have been", "could be", "may have been",
            "approximately", "around", "about", "roughly",
        ]
        
        for phrase in confabulation_phrases:
            if phrase.lower() in probe_response.lower():
                attribution["confabulation_markers"].append({
                    "phrase": phrase,
                    "context": self._get_surrounding_context(probe_response, phrase),
                })
        
        # Detect confidence patterns
        confidence_phrases = {
            "high": ["definitely", "certainly", "clearly", "indeed", "specifically", "exactly"],
            "medium": ["generally", "mostly", "mainly", "primarily", "typically"],
            "low": ["perhaps", "seems", "appears", "not sure", "unclear", "vaguely"],
        }
        
        for confidence_level, phrases in confidence_phrases.items():
            for phrase in phrases:
                if phrase.lower() in probe_response.lower():
                    attribution["confidence_patterns"].append({
                        "level": confidence_level,
                        "phrase": phrase,
                        "context": self._get_surrounding_context(probe_response, phrase),
                    })
        
        return attribution
    
    def _detect_hallucination(self, memory_text: str, probe_response: str) -> Dict[str, Any]:
        """
        Detect hallucination in memory recall.
        
        Args:
            memory_text: Original memory text
            probe_response: Model's probe response
            
        Returns:
            Hallucination detection results
            
        ⇌ Hallucination detection maps the boundary between memory and confabulation ⇌
        """
        # Initialize hallucination detection
        hallucination = {
            "detected": False,
            "details": None,
        }
        
        # Extract key facts from memory text for contradiction detection
        import re
        
        # Define key patterns to extract factual information
        fact_patterns = {
            "founding_year": r"founded in (\d{4})",
            "founder": r"founded in \d{4} by (Dr\. [A-Za-z\s]+)",
            "departments": r"(\d+) main departments",
            "location": r"headquarters is located in ([A-Za-z, ]+)",
            "address": r"at (\d+ [A-Za-z\s]+)",
            "budget": r"\$(\d+\.?\d*) million",
            "study_year": r"published in (\d{4})",
            "participants": r"(\d+,?\d*) participants",
            "countries": r"across (\d+) countries",
            "director": r"director is (Dr\. [A-Za-z\s]+)",
            "start_year": r"took over in (\d{4})",
            "researchers": r"employs (\d+) researchers",
            "partnerships": r"partnerships with (\d+) universities",
            "database_records": r"(\d+,?\d*) experiments",
        }
        
        # Extract reference facts
        reference_facts = {}
        for key, pattern in fact_patterns.items():
            match = re.search(pattern, memory_text)
            if match:
                reference_facts[key] = match.group(1)
        
        # Look for contradictions in the probe response
        contradictions = []
        fabrications = []
        
        # Check for contradictions with reference facts
        for key, value in reference_facts.items():
            # Construct pattern to find potential contradictions
            # This looks for the key concept followed by a different value
            concept_map = {
                "founding_year": r"founded in (\d{4})",
                "founder": r"founded by (Dr\. [A-Za-z\s]+)",
                "departments": r"(\d+) departments",
                "location": r"located in ([A-Za-z, ]+)",
                "address": r"at (\d+ [A-Za-z\s]+)",
                "budget": r"\$(\d+\.?\d*) million",
                "study_year": r"published in (\d{4})",
                "participants": r"(\d+,?\d*) participants",
                "countries": r"across (\d+) countries",
                "director": r"director is (Dr\. [A-Za-z\s]+)",
                "start_year": r"took over in (\d{4})",
                "researchers": r"employs (\d+) researchers",
                "partnerships": r"partnerships with (\d+) universities",
                "database_records": r"(\d+,?\d*) experiments",
            }
            
            # Skip if no concept pattern
            if key not in concept_map:
                continue
            
            # Find potential contradicting values
            for match in re.finditer(concept_map[key], probe_response):
                found_value = match.group(1)
                
                # Clean values for comparison (remove commas in numbers)
                clean_found = found_value.replace(',', '') if re.match(r'\d+,\d+', found_value) else found_value
                clean_ref = value.replace(',', '') if re.match(r'\d+,\d+', value) else value
                
                # Check if the values are different
                if clean_found != clean_ref:
                    contradictions.append({
                        "fact": key,
                        "reference_value": value,
                        "hallucinated_value": found_value,
                        "context": self._get_surrounding_context(probe_response, found_value),
                    })
        
        # Look for fabricated details (information not in original memory text)
        # This is more challenging but we can look for specific patterns
        
        # Names not in original text
        memory_names = re.findall(r'Dr\. ([A-Za-z\s]+)', memory_text)
        response_names = re.findall(r'Dr\. ([A-Za-z\s]+)', probe_response)
        
        for name in response_names:
            if name not in memory_names:
                fabrications.append({
                    "type": "fabricated_name",
                    "value": f"Dr. {name}",
                    "context": self._get_surrounding_context(probe_response, f"Dr. {name}"),
                })
        
        # Years not in original text
        memory_years = re.findall(r'\b(19|20)\d{2}\b', memory_text)
        response_years = re.findall(r'\b(19|20)\d{2}\b', probe_response)
        
        for year in response_years:
            if year not in memory_years:
                fabrications.append({
                    "type": "fabricated_year",
                    "value": year,
                    "context": self._get_surrounding_context(probe_response, year),
                })
        
        # Complete detection
        if contradictions or fabrications:
            hallucination["detected"] = True
            hallucination["details"] = {
                "contradictions": contradictions,
                "fabrications": fabrications,
            }
        
        return hallucination
    
    def _map_attribution(self, decay_results: List[Dict[str, Any]], probe_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create a comprehensive attribution map across decay levels.
        
        Args:
            decay_results: Results from decay testing
            probe_results: Results from memory probing
            
        Returns:
            Attribution map
            
        ⧖ Attribution mapping stabilizes decay path tracing ⧖
        """
        # Initialize attribution map
        attribution_map = {
            "decay_curve": {
                "levels": [r["level"] for r in decay_results],
                "accuracy": [r["recall_accuracy"] for r in decay_results],
            },
            "transition_points": [],
            "attribution_paths": [],
        }
        
        # Find transition points (significant changes in recall accuracy)
        accuracies = [r["recall_accuracy"] for r in decay_results]
        for i in range(1, len(accuracies)):
            delta = accuracies[i] - accuracies[i-1]
            if abs(delta) > 0.2:  # Significant change
                attribution_map["transition_points"].append({
                    "from_level": i,
                    "to_level": i+1,
                    "delta": delta,
                    "from_accuracy": accuracies[i-1],
                    "to_accuracy": accuracies[i],
                })
        
        # Analyze attribution paths from probe results
        for probe in probe_results:
            if "attribution" in probe and "source_traces" in probe["attribution"]:
                for trace in probe["attribution"]["source_traces"]:
                    attribution_map["attribution_paths"].append({
                        "type": trace["type"],
                        "value": trace["value"],
                        "probe_index": probe["probe_index"],
                        "context": trace["context"],
                    })
            
            # Include hallucination paths
            if "hallucination_detected" in probe and probe["hallucination_detected"]:
                if "hallucination_details" in probe and probe["hallucination_details"]:
                    details = probe["hallucination_details"]
                    
                    # Add contradictions
                    for contradiction in details.get("contradictions", []):
                        attribution_map["attribution_paths"].append({
                            "type": "contradiction",
                            "fact": contradiction["fact"],
                            "reference": contradiction["reference_value"],
                            "hallucinated": contradiction["hallucinated_value"],
                            "probe_index": probe["probe_index"],
                            "context": contradiction["context"],
                        })
                    
                    # Add fabrications
                    for fabrication in details.get("fabrications", []):
                        attribution_map["attribution_paths"].append({
                            "type": "fabrication",
                            "value_type": fabrication["type"],
                            "value": fabrication["value"],
                            "probe_index": probe["probe_index"],
                            "context": fabrication["context"],
                        })
        
        return attribution_map
    
    def _extract_attribution_patterns(self, probe_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Extract attribution patterns from probe results.
        
        Args:
            probe_results: Results from memory probing
            
        Returns:
            List of attribution patterns
            
        ↻ Pattern extraction recursively traces meaning across decay ↻
        """
        # Initialize patterns
        patterns = []
        
        # Track confidence markers
        confidence_distribution = {"high": 0, "medium": 0, "low": 0}
        
        # Track attribution sources
        attribution_sources = {"memory": 0, "confabulation": 0, "fabrication": 0}
        
        # Extract patterns from all probes
        for probe in probe_results:
            # Skip if missing attribution data
            if "attribution" not in probe:
                continue
            
            attribution = probe["attribution"]
            
            # Count confidence levels
            for confidence in attribution.get("confidence_patterns", []):
                confidence_distribution[confidence["level"]] += 1
            
            # Count confabulation markers
            confabulation_count = len(attribution.get("confabulation_markers", []))
            
            # Count source traces
            source_trace_count = len(attribution.get("source_traces", []))
            
            # Update attribution sources
            if source_trace_count > confabulation_count:
                attribution_sources["memory"] += 1
            elif confabulation_count > 0:
                attribution_sources["confabulation"] += 1
            
            # Count fabrications from hallucination detection
            if probe.get("hallucination_detected", False) and probe.get("hallucination_details"):
                details = probe["hallucination_details"]
                fabrication_count = len(details.get("fabrications", []))
                if fabrication_count > 0:
                    attribution_sources["fabrication"] += 1
        
        # Create pattern for confidence distribution
        patterns.append({
            "type": "confidence_distribution",
            "distribution": confidence_distribution,
        })
        
        # Create pattern for attribution sources
        patterns.append({
            "type": "attribution_sources",
            "distribution": attribution_sources,
        })
        
        # Create pattern for transitions between memory and confabulation
        if probe_results and all(p.get("hallucination_detected") is not None for p in probe_results):
            transitions = []
            prev_state = None
            
            for i, probe in enumerate(probe_results):
                current_state = "hallucination" if probe.get("hallucination_detected", False) else "memory"
                
                if prev_state is not None and prev_state != current_state:
                    transitions.append({
                        "from": prev_state,
                        "to": current_state,
                        "probe_index": i,
                    })
                
                prev_state = current_state
            
            if transitions:
                patterns.append({
                    "type": "memory_to_hallucination_transitions",
                    "transitions": transitions,
                })
        
        return patterns
    
    def _identify_hallucination_transition(self, decay_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Identify the transition point where memory decay leads to hallucination.
        
        Args:
            decay_results: Results from decay testing
            
        Returns:
            Hallucination transition information
            
        🜏 Transition identification mirrors the memory-hallucination boundary 🜏
        """
        # Default values
        hallucination_transition = {
            "identified": False,
            "transition_point": None,
            "accuracy_threshold": None,
        }
        
        # Extract accuracy curve
        accuracies = [(r["level"], r["recall_accuracy"]) for r in decay_results]
        
        # Sort by level
        accuracies.sort(key=lambda x: x[0])
        
        # Find the steepest decline in accuracy
        max_decline = 0
        transition_idx = None
        
        for i in range(1, len(accuracies)):
            level_prev, acc_prev = accuracies[i-1]
            level_curr, acc_curr = accuracies[i]
            
            decline = acc_prev - acc_curr
            
            if decline > max_decline:
                max_decline = decline
                transition_idx = i
        
        # If we found a significant decline (>20%), mark as transition point
        if max_decline > 0.2 and transition_idx is not None:
            transition_level = accuracies[transition_idx][0]
            transition_accuracy = accuracies[transition_idx][1]
            
            hallucination_transition = {
                "identified": True,
                "transition_point": transition_level,
                "accuracy_threshold": transition_accuracy,
                "decline_magnitude": max_decline,
            }
        
        return hallucination_transition
    
    def _get_surrounding_context(self, text: str, target: str, window: int = 50) -> str:
        """
        Get surrounding context for a target string in text.
        
        Args:
            text: Source text
            target: Target string to find
            window: Character window around target
            
        Returns:
            Context string with target highlighted
        """
        try:
            target_pos = text.find(target)
            if target_pos == -1:
                # Try case-insensitive search
                target_pos = text.lower().find(target.lower())
                if target_pos == -1:
                    return ""
            
            start = max(0, target_pos - window)
            end = min(len(text), target_pos + len(target) + window)
            
            # Create context with markers
            context = text[start:target_pos] + "**" + text[target_pos:target_pos + len(target)] + "**" + text[target_pos + len(target):end]
            
            return context.strip()
        except Exception:
            return ""
    
    def _generate_id(self, content: str) -> str:
        """
        Generate a unique ID for shell execution.
        
        Args:
            content: Content to generate ID from
            
        Returns:
            Unique ID string
            
        🝚 ID generation creates persistent symbolic reference 🝚
        """
        # Create hash from content and timestamp
        hash_input = f"{content}{time.time()}"
        
        # Generate hash
        import hashlib
        return "memtrace_" + hashlib.md5(hash_input.encode()).hexdigest()[:8]
