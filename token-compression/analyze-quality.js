import { encoding_for_model } from "tiktoken";

const enc = await encoding_for_model("o4-mini");

const concepts = [
  {
    name: "1. Entropía Termodinámica",
    natural: "thermodynamic entropy is proportional to the logarithm of the number of microstates",
    compressed: "S = k_B ln(Ω)",
    concepts: ["S", "k_B", "ln", "Ω", "proportional", "thermodynamic", "microstates"],
    technical_terms: ["S", "k_B", "ln", "Ω", "thermodynamic entropy"],
  },
  {
    name: "2. Entropía de Información",
    natural: "information entropy is the negative sum of probability times log probability",
    compressed: "H = -Σ p_i log₂(p_i)",
    concepts: ["H", "Σ", "p_i", "log", "probability", "negative", "sum"],
    technical_terms: ["H", "Σ", "p_i", "log₂", "information entropy"],
  },
  {
    name: "3. Fuerza Conservativa",
    natural: "a conservative force is equal to the negative gradient of potential energy",
    compressed: "F = -∇U",
    concepts: ["F", "∇", "U", "conservative", "force", "gradient", "potential", "energy"],
    technical_terms: ["F", "-∇U", "conservative force", "potential energy"],
  },
  {
    name: "4. Consensus BFT",
    natural: "byzantine fault tolerance means the system is correct as long as fewer than one third of the nodes are faulty",
    compressed: "BFT: correct iff f < n/3",
    concepts: ["correct", "faulty", "nodes", "threshold", "one third", "BFT", "Byzantine"],
    technical_terms: ["BFT", "f < n/3", "fault tolerance", "correct iff"],
  },
  {
    name: "5. DAG",
    natural: "in a directed acyclic graph all edges go from a node with lower rank to a node with higher rank",
    compressed: "DAG: ∀(u,v)∈E: rank(u) < rank(v)",
    concepts: ["edges", "rank", "lower", "higher", "acyclic", "directed", "graph", "node"],
    technical_terms: ["DAG", "∀(u,v)∈E", "rank(u) < rank(v)", "acyclic"],
  },
  {
    name: "6. Segunda Ley",
    natural: "the second law of thermodynamics states that entropy change with respect to time is always greater than or equal to zero",
    compressed: "∂S/∂t ≥ 0",
    concepts: ["entropy", "time", "change", "second law", "thermodynamics", "greater", "zero"],
    technical_terms: ["∂S/∂t", "≥ 0", "second law", "entropy"],
  },
  {
    name: "7. E=mc²",
    natural: "mass energy equivalence states that the energy of a system is equal to its mass times the speed of light squared",
    compressed: "E = mc²",
    concepts: ["mass", "energy", "equivalence", "speed of light", "squared", "E", "m", "c"],
    technical_terms: ["E", "mc²", "mass-energy equivalence", "c²"],
  },
  {
    name: "8. Schrödinger",
    natural: "the time-independent Schrödinger equation relates the Laplacian of the wave function to the difference between total energy and potential energy",
    compressed: "∇²ψ + (2m/ℏ²)(E-V)ψ = 0",
    concepts: ["Schrödinger", "wave function", "Laplacian", "energy", "potential", "mass", "Planck"],
    technical_terms: ["∇²ψ", "(2m/ℏ²)", "E-V", "Schrödinger equation"],
  },
  {
    name: "9. Python List Comprehension",
    natural: "list comprehension that applies a function to each element in a data collection where a predicate condition holds",
    compressed: "[f(x) for x in data if P(x)]",
    concepts: ["function", "element", "data", "condition", "predicate", "list", "comprehension"],
    technical_terms: ["[f(x)", "for x in", "if P(x)]", "list comprehension"],
  },
  {
    name: "10. Lean Theorem",
    natural: "there exists a convergence point k such that for all indices j greater than or equal to k the function value equals the limit",
    compressed: "∃ k, ∀ j ≥ k: f(j) = f(k)",
    concepts: ["exists", "for all", "convergence", "limit", "index", "k", "j"],
    technical_terms: ["∃ k", "∀ j ≥ k", "f(j) = f(k)", "convergence"],
  },
];

console.log("=== ANÁLISIS DE DENSIDAD INFORMACIONAL ===\n");

let totalNaturalTokens = 0;
let totalCompressedTokens = 0;
let totalConceptsNatural = 0;
let totalConceptsCompressed = 0;
let totalTechnicalNatural = 0;
let totalTechnicalCompressed = 0;

for (const item of concepts) {
  const naturalTokens = enc.encode(item.natural).length;
  const compressedTokens = enc.encode(item.compressed).length;
  
  const densityNatural = item.concepts.length / naturalTokens;
  const densityCompressed = item.concepts.length / compressedTokens;
  
  const technicalDensityNatural = item.technical_terms.length / naturalTokens;
  const technicalDensityCompressed = item.technical_terms.length / compressedTokens;
  
  const improvement = ((densityCompressed - densityNatural) / densityNatural * 100);
  const technicalImprovement = ((technicalDensityCompressed - technicalDensityNatural) / technicalDensityNatural * 100);

  console.log(`\n${item.name}`);
  console.log("  Natural:  ", item.natural);
  console.log("  Comprim:  ", item.compressed);
  console.log(`  Tokens:   ${naturalTokens} → ${compressedTokens} (${naturalTokens - compressedTokens > 0 ? '+' : ''}${naturalTokens - compressedTokens})`);
  console.log(`  Densidad conceptual: ${densityNatural.toFixed(3)} → ${densityCompressed.toFixed(3)} (${improvement > 0 ? '+' : ''}${improvement.toFixed(1)}%)`);
  console.log(`  Densidad técnica:    ${technicalDensityNatural.toFixed(3)} → ${technicalDensityCompressed.toFixed(3)} (${technicalImprovement > 0 ? '+' : ''}${technicalImprovement.toFixed(1)}%)`);

  totalNaturalTokens += naturalTokens;
  totalCompressedTokens += compressedTokens;
  totalConceptsNatural += item.concepts.length;
  totalConceptsCompressed += item.concepts.length;
  totalTechnicalNatural += item.technical_terms.length;
  totalTechnicalCompressed += item.technical_terms.length;
}

console.log("\n" + "=".repeat(70));
console.log("=== RESUMEN: CALIDAD INFORMACIONAL ===");
console.log("=".repeat(70));

const avgDensityNatural = totalConceptsNatural / totalNaturalTokens;
const avgDensityCompressed = totalConceptsCompressed / totalCompressedTokens;
const avgTechnicalNatural = totalTechnicalNatural / totalNaturalTokens;
const avgTechnicalCompressed = totalTechnicalCompressed / totalCompressedTokens;

console.log(`\nTokens totales:        ${totalNaturalTokens} → ${totalCompressedTokens}`);
console.log(`Densidad conceptual:  ${avgDensityNatural.toFixed(4)} → ${avgDensityCompressed.toFixed(4)} conceptos/token`);
console.log(`Densidad técnica:     ${avgTechnicalNatural.toFixed(4)} → ${avgTechnicalCompressed.toFixed(4)} términos técnicos/token`);

console.log("\n" + "=".repeat(70));
console.log("=== MÉTRICAS PROPUESTAS PARA EVALUAR CALIDAD ===");
console.log("=".repeat(70));

console.log(`
MÉTRICA 1: Densidad Informacional (DI)
  DI = conceptos_preservados / tokens_usados
  La versión comprimida tiene ${((avgDensityCompressed/avgDensityNatural - 1)*100).toFixed(1)}% más conceptos por token

MÉTRICA 2: Densidad Técnica (DT)
  DT = terminos_técnicos_preservados / tokens
  Mide precisión científica. Mejora: ${((avgTechnicalCompressed/avgTechnicalNatural - 1)*100).toFixed(1)}%

MÉTRICA 3: Precisión Semántica (PS)
  ¿La notación formal captura exactamente el concepto sin ambigüedad?
  - Notación math/código: tipos enforceados, sin ambigüedad léxica
  - Lenguaje natural: ambiguo, requiere contexto

MÉTRICA 4: Fidelidad Reproducible (FR)
  ¿El receptor puede reconstruir el concepto exactamente?
  - f = -∇U siempre significa lo mismo
  - "fuerza conservativa" puede interpretarse de muchas formas

MÉTRICA 5: Compresibilidad vs Comprensibilidad (CC)
  CC = (tokens_ahorrados * comprensibilidad) / complejidad_adicional
  Para Fran (experto): alta comprensibilidad = alto valor
`);

console.log("\n=== RECOMENDACIÓN PARA LA SKILL ===");
console.log("=".repeat(70));
console.log(`
CONCLUSIONES:
1. La notación formal NO siempre ahorra tokens
2. PERO mejora significativamente la densidad informacional:
   - Más conceptos por token gastado
   - Más términos técnicos precisos por token
3. ParaFran (experto en termodinámica/-info/CHIMERA):
   - Notación formal = más útil aunque gaste mismos tokens
   - Porque preserva precisión que lenguaje natural pierde

MÉTRICA COMPUESTA SUGERIDA:
  Valor_Real = (conceptos_preservados * precision) / tokens - (complejidad * esfuerzo_decode)
  
  Para experto: complejidad_decode ≈ 0
  Para novato: complejidad_decode > 0
`);
