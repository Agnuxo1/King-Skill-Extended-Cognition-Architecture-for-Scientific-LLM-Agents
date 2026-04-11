import { encoding_for_model } from "tiktoken";

const enc = await encoding_for_model("o4-mini");

const compressions = [
  {
    name: "1. Mathematics & Physics",
    natural: [
      "thermodynamic entropy is proportional to the logarithm of the number of microstates",
      "information entropy is the negative sum of probability times log probability",
      "mutual information equals entropy of X minus conditional entropy of X given Y",
      "KL divergence measures the difference between two probability distributions",
      "conservative force is the negative gradient of potential energy",
      "the second law states that entropy change over time is greater than or equal to zero",
      "energy is equal to Planck's constant times frequency",
      "mass energy equivalence states that mass times the speed of light squared equals energy",
      "the Schrödinger equation describes the quantum wave function",
    ],
    compressed: [
      "S = k_B ln(Ω)",
      "H = -Σ p_i log₂(p_i)",
      "I(X;Y) = H(X) - H(X|Y)",
      "D_KL(P‖Q) = Σ P log(P/Q)",
      "F = -∇U",
      "∂S/∂t ≥ 0",
      "E = hf = ℏω",
      "E = mc²",
      "∇²ψ + (2m/ℏ²)(E-V)ψ = 0",
    ],
  },
  {
    name: "2. Python Pseudocode",
    natural: [
      "use a conditional expression to choose between A and B",
      "iterate while the state has not converged and update the state each time",
      "list comprehension that applies function f to each element x in data where predicate P holds",
      "use reduce to combine map and filter operations on data",
      "dictionary comprehension from pairs where a condition holds",
      "define a function to solve a graph with tolerance and return a solution",
    ],
    compressed: [
      "result = A if condition else B",
      "while not converged(state): state = update(state)",
      "[f(x) for x in data if P(x)]",
      "result = reduce(g, map(f, filter(P, data)))",
      "{k: v for k, v in pairs if condition}",
      "def solve(graph: DAG, tol: float = 1e-6) -> Solution: ...",
    ],
  },
  {
    name: "3. Lean 4 / Formal Logic",
    natural: [
      "theorem stating consensus convergence: for all i the function f of i is valid, therefore there exists k such that for all j greater than or equal to k the function f of j equals the function f of k",
      "define a structure for peer review with fields for claim, verified boolean, score float, and seventeen judges",
    ],
    compressed: [
      "theorem consensus_convergence (n : ℕ) (h : ∀ i, valid (f i)) : ∃ k, ∀ j ≥ k, f j = f k := by sorry",
      "structure PeerReview where claim : Prop; verified : Bool; score : Float; judges : Fin 17",
    ],
  },
  {
    name: "4. Graphs & Distributed Systems",
    natural: [
      "a graph consists of vertices, edges, and a weight function",
      "in a directed acyclic graph for all edges the rank of the source is less than the rank of the target",
      "consensus means that as time approaches infinity all states converge to the same value",
      "byzantine fault tolerance requires that the number of faulty nodes is less than one third of total nodes",
      "in a peer to peer network every node has degree at least k minimum",
      "independence means that for all different indices i and j the judgments of judge i are independent of judge j",
    ],
    compressed: [
      "G = (V, E, w)",
      "DAG: ∀(u,v)∈E: rank(u) < rank(v)",
      "consensus: ∀i,j: lim_{t→∞} state_i(t) = state_j(t)",
      "BFT: correct iff f < n/3",
      "P2P: ∀node_i: degree(i) ≥ k_min",
      "independence: ∀i≠j: judge_i ⊥ judge_j",
    ],
  },
  {
    name: "5. Complexity",
    natural: [
      "constant time is less than logarithmic time which is less than linear time which is less than linearithmic time which is less than quadratic time which is less than cubic time which is less than exponential time",
      "there is a space-time tradeoff where the product of space and time is at least a constant value",
    ],
    compressed: [
      "O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(n³) < O(2ⁿ)",
      "space-time tradeoff: S × T ≥ k",
    ],
  },
  {
    name: "6. Emoji Dictionary",
    natural: [
      "verified or correct",
      "falsified or incorrect",
      "implies or next step",
      "iteration or loop",
      "failure or stop",
      "pass or ok",
      "partial or warning",
      "hypothesis or idea",
      "objective",
      "invariant or fixpoint",
      "fast or efficient",
      "hard constraint",
      "delta or change",
      "merge or combine",
    ],
    compressed: [
      "✓",
      "✗",
      "→",
      "↺",
      "🔴",
      "🟢",
      "🟡",
      "💡",
      "🎯",
      "📌",
      "⚡",
      "🧱",
      "△",
      "⊕",
    ],
  },
  {
    name: "7. Chinese Chengyu",
    natural: [
      "different methods achieving the same result",
      "mutual reinforcement between A and B (synergy)",
      "few-shot generalization capability",
      "ensemble of methods (like seventeen judges in OpenCLAW)",
      "peer-review and noise filtering",
      "iterative convergence process",
      "theory and experiment aligned together",
      "case leading to generalization",
      "post-hoc necessary fix",
      "causal relation",
    ],
    compressed: [
      "异曲同工",
      "相辅相成",
      "举一反三",
      "博采众长",
      "去伪存真",
      "循序渐进",
      "知行合一",
      "以点带面",
      "亡羊补牢",
      "因果关系",
    ],
  },
  {
    name: "8. Domain-specific Notations",
    natural: [
      "SMILES notation for aspirin molecular structure is CC(=O)Oc1ccccc1C(=O)O",
      "regular expression pattern matching two uppercase letters followed by four digits",
      "cron expression meaning every six hours",
      "JSON object with key value pairs",
      "function signature from A to B to C",
      "Dirac notation for quantum expectation value",
    ],
    compressed: [
      "CC(=O)Oc1ccccc1C(=O)O",
      "^[A-Z]{2}\\d{4}$",
      "0 */6 * * *",
      "{\"k\": v, \"k2\": v2}",
      "f : A → B → C",
      "⟨ψ|H|ψ⟩ = E",
    ],
  },
  {
    name: "Quick Substitution Table",
    natural: [
      "in other words",
      "therefore",
      "because",
      "which means",
      "if and only if",
      "for all x in S",
      "there exists x such that",
      "tends to zero as x approaches infinity",
      "grows with X",
      "approximately equal to",
      "much greater than",
      "defined as",
      "probability of X given Y",
      "expectation of X",
      "variance of X",
      "independent peer review means judgments are independent",
      "Byzantine fault tolerant means correct if and only if faulty nodes are less than one third",
      "decreasing returns means second derivative is negative",
      "converges to fixed point means there exists a point where function equals itself",
    ],
    compressed: [
      "⟺",
      "∴",
      "∵",
      "⟹",
      "⟺",
      "∀x ∈ S",
      "∃x:",
      "→ 0",
      "∝ X",
      "≈",
      "≫",
      "≡",
      "P(X|Y)",
      "𝔼[X]",
      "Var(X)",
      "∀i≠j: judge_i ⊥ judge_j",
      "correct iff f < n/3",
      "d²f/dx² < 0",
      "∃x*: f(x*) = x*",
    ],
  },
];

console.log("=== TOKEN COMPRESSION ANALYSIS ===\n");

let totalNatural = 0;
let totalCompressed = 0;

for (const category of compressions) {
  console.log(`\n## ${category.name}`);
  console.log("-".repeat(60));

  const naturalTokens = enc.encode(category.natural.join(" ")).length;
  const compressedTokens = enc.encode(category.compressed.join(" ")).length;

  const savings = naturalTokens - compressedTokens;
  const percentage = ((savings / naturalTokens) * 100).toFixed(1);

  console.log(`Natural tokens:     ${naturalTokens}`);
  console.log(`Compressed tokens:  ${compressedTokens}`);
  console.log(`Ahorro:           ${savings} tokens (${percentage}%)`);

  console.log("\n--- Ejemplos detallados ---");
  for (let i = 0; i < Math.min(3, category.natural.length); i++) {
    const nTokens = enc.encode(category.natural[i]).length;
    const cTokens = enc.encode(category.compressed[i]).length;
    console.log(`  "${category.natural[i]}" -> ${nTokens} tokens`);
    console.log(`  "${category.compressed[i]}" -> ${cTokens} tokens`);
    console.log(`  Ahorro: ${nTokens - cTokens} tokens\n`);
  }

  totalNatural += naturalTokens;
  totalCompressed += compressedTokens;
}

console.log("\n" + "=".repeat(60));
console.log("=== RESUMEN TOTAL ===");
console.log("=".repeat(60));
console.log(`Total natural:      ${totalNatural} tokens`);
console.log(`Total compress:     ${totalCompressed} tokens`);
console.log(`AHORRO TOTAL:     ${totalNatural - totalCompressed} tokens (${((totalNatural - totalCompressed) / totalNatural * 100).toFixed(1)}%)`);

console.log("\n=== MEDIA POR APARTADO ===");
for (const category of compressions) {
  const naturalTokens = enc.encode(category.natural.join(" ")).length;
  const compressedTokens = enc.encode(category.compressed.join(" ")).length;
  const savings = naturalTokens - compressedTokens;
  const avgPerItem = (savings / category.natural.length).toFixed(1);
  console.log(`${category.name}: ${avgPerItem} tokens/elemento de media`);
}