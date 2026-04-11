import { encoding_for_model } from "tiktoken";

const enc = await encoding_for_model("o4-mini");

console.log("=== ANÁLISIS COMPLETO TOKEN COMPRESSION v4 (CON QUÍMICA) ===\n");

const chemistryTests = [
  {
    domain: "Chemistry - Elements",
    natural: "hydrogen oxygen nitrogen carbon sulfur phosphorus iron copper zinc gold silver lead mercury silicon chlorine sodium potassium calcium magnesium aluminum",
    compressed: "H O N C S Fe Cu Zn Au Ag Pb Hg Si Na K Ca Mg Al",
    tokens: "Periodic table elements"
  },
  {
    domain: "Chemistry - Molecules",
    natural: "water carbon dioxide oxygen nitrogen hydrogen chlorine sodium chloride sulfuric acid nitric acid phosphoric acid sodium hydroxide potassium hydroxide ammonia",
    compressed: "H₂O CO₂ O₂ N₂ H₂ Cl₂ NaCl H₂SO₄ HNO₃ H₃PO₄ NaOH KOH NH₃",
    tokens: "Common inorganic molecules"
  },
  {
    domain: "Chemistry - Organic",
    natural: "methane ethane propane ethylene acetylene benzene methanol ethanol propanol acetic acid formic acid glucose sucrose caffeine aspirin",
    compressed: "CH₄ C₂H₆ C₃H₈ C₂H₄ C₂H₂ C₆H₆ CH₃OH C₂H₅OH C₃H₇OH CH₃COOH HCOOH C₆H₁₂O₁₂ C₁₂H₂₂O₁₁ C₈H₁₀N₄O₂ CC(=O)Oc1ccccc1C(=O)O",
    tokens: "Organic compounds"
  },
  {
    domain: "Chemistry - Reactions",
    natural: "glucose combustion produces carbon dioxide and water: one molecule of glucose plus six molecules of oxygen yield six molecules of carbon dioxide plus six molecules of water",
    compressed: "C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O",
    tokens: "Combustion reaction"
  },
  {
    domain: "Chemistry - Thermodynamics",
    natural: "Gibbs free energy change equals enthalpy change minus temperature times entropy change, and the standard Gibbs free energy equals minus RT times the natural logarithm of the equilibrium constant",
    compressed: "ΔG = ΔH - TΔS | ΔG° = -RT ln K",
    tokens: "Chemical thermodynamics"
  },
  {
    domain: "Chemistry - Acid-Base",
    natural: "pH is defined as the negative logarithm of hydrogen ion concentration, and the Henderson-Hasselbalch equation relates pH to pKa and the ratio of conjugate base to acid",
    compressed: "pH = -log[H⁺] | pH = pKa + log([A⁻]/[HA])",
    tokens: "Acid-base chemistry"
  },
  {
    domain: "Chemistry - Electrochemistry",
    natural: "the standard cell potential equals the difference between cathode and anode potentials, and the Gibbs free energy change equals minus n times Faraday constant times cell potential",
    compressed: "E°cell = E°cathode - E°anode | ΔG = -nFE°",
    tokens: "Electrochemistry"
  },
  {
    domain: "Chemistry - Kinetics",
    natural: "reaction rate equals rate constant times concentration of reactants raised to their reaction order, and the rate constant follows Arrhenius dependence on temperature with activation energy",
    compressed: "r = k[A]^m[B]^n | k = Ae^(-Ea/RT)",
    tokens: "Chemical kinetics"
  },
  {
    domain: "Chemistry - SMILES Complex",
    natural: "caffeine molecule has a purine core with two methyl groups and two carbonyl groups giving formula C8H10N4O2 and SMILES notation Cn1c(=O)c2c(ncn2C)n(c1=O)C",
    compressed: "C₈H₁₀N₄O₂ | Cn1c(=O)c2c(ncn2C)n(c1=O)C",
    tokens: "Complex molecule SMILES"
  },
  {
    domain: "Chemistry - Nuclear",
    natural: "uranium-235 undergoes fission when absorbing a neutron, producing barium-141, krypton-92, three neutrons and releasing approximately 200 MeV of energy per fission event",
    compressed: "²³⁵U + n → ¹⁴¹Ba + ⁹²Kr + 3n + 200 MeV",
    tokens: "Nuclear fission"
  }
];

console.log("=== CHEMISTRY COMPRESSION RESULTS ===\n");

let chemTotalNatural = 0;
let chemTotalCompressed = 0;

for (const test of chemistryTests) {
  const naturalTokens = enc.encode(test.natural).length;
  const compressedTokens = enc.encode(test.compressed).length;
  const savings = naturalTokens - compressedTokens;
  const percent = ((savings / naturalTokens) * 100).toFixed(1);
  
  console.log(`${test.domain}`);
  console.log(`  Natural:     ${naturalTokens} tokens`);
  console.log(`  Compressed: ${compressedTokens} tokens`);
  console.log(`  Savings:     ${savings > 0 ? '+' : ''}${savings} (${percent}%)`);
  console.log(`  Type:        ${test.tokens}\n`);
  
  chemTotalNatural += naturalTokens;
  chemTotalCompressed += compressedTokens;
}

console.log("=".repeat(60));
console.log("CHEMISTRY TOTAL:");
console.log(`  Natural:     ${chemTotalNatural} tokens`);
console.log(`  Compressed: ${chemTotalCompressed} tokens`);
console.log(`  TOTAL SAVINGS: ${chemTotalNatural - chemTotalCompressed} (${((chemTotalNatural - chemTotalCompressed)/chemTotalNatural*100).toFixed(1)}%)`);
console.log("=".repeat(60));

console.log("\n=== P2PCLAW REALISTIC PAPER SCENARIO ===\n");

const paperTokens = 3000;
const reasoningTokens = 25000;
const totalTokensWithoutCompression = reasoningTokens + paperTokens;

console.log(`P2PCLAW Requirements:`);
console.log(`  Minimum paper output: 2,500 tokens`);
console.log(`  Average paper output: 3,000 tokens`);
console.log(`  Reasoning tokens per paper: ~25,000 (experiments, verification)`);
console.log(`  Total tokens per paper (without compression): ${totalTokensWithoutCompression}`);

const reasonCompressionRate = 0.15;
const outputCompressionRate = 0.33;

const reasoningCompressed = reasoningTokens * (1 - reasonCompressionRate);
const outputCompressed = paperTokens * (1 - outputCompressionRate);
const totalCompressed = reasoningCompressed + outputCompressed;
const totalSavings = totalTokensWithoutCompression - totalCompressed;

console.log(`\nWith Compression:`);
console.log(`  Reasoning compressed: ${reasoningCompressed.toFixed(0)} (-${(reasonCompressionRate*100).toFixed(0)}%)`);
console.log(`  Output compressed:    ${outputCompressed.toFixed(0)} (-${(outputCompressionRate*100).toFixed(0)}%)`);
console.log(`  Total with compression: ${totalCompressed.toFixed(0)}`);
console.log(`  TOTAL SAVINGS: ${totalSavings.toFixed(0)} tokens/paper (${(totalSavings/totalTokensWithoutCompression*100).toFixed(1)}%)`);

console.log("\n=== COST ANALYSIS WITH 10 MODELS ===\n");

const models = [
  { name: "DeepSeek V3", input: 0.14, output: 0.28 },
  { name: "Gemini 2.5 Flash", input: 0.15, output: 0.60 },
  { name: "Mistral Small 3.1", input: 0.20, output: 0.60 },
  { name: "DeepSeek R1", input: 0.55, output: 2.19 },
  { name: "GPT-5.4 Mini", input: 0.75, output: 4.50 },
  { name: "Mistral Large 3", input: 2.00, output: 6.00 },
  { name: "Gemini 2.5 Pro", input: 1.25, output: 10.00 },
  { name: "Claude Sonnet 4.6", input: 3.00, output: 15.00 },
  { name: "GPT-5.4", input: 2.50, output: 15.00 },
  { name: "Claude Opus 4.6", input: 15.00, output: 75.00 }
];

const inputRatio = 0.30;
const outputRatio = 0.70;

console.log("Per Paper Cost Analysis (28,000 tokens total):\n");
console.log("| Model | No Compression | With Compression | Savings/Paper | Annual (1000/day) |");
console.log("|-------|---------------|------------------|----------------|-------------------|");

for (const model of models) {
  const blendedRate = (model.input * inputRatio + model.output * outputRatio) / 1e6;
  const costNoCompression = totalTokensWithoutCompression * blendedRate;
  const costWithCompression = totalCompressed * blendedRate;
  const savingsPerPaper = costNoCompression - costWithCompression;
  const annualSavings = savingsPerPaper * 1000 * 365;
  
  console.log(`| ${model.name.padEnd(20)} | $${costNoCompression.toFixed(4)} | $${costWithCompression.toFixed(4)} | $${savingsPerPaper.toFixed(4)} | $${annualSavings.toFixed(2)} |`);
}

console.log("\n=== REASONING QUALITY IMPROVEMENT ===\n");

const reasoningImprovements = [
  {
    concept: "Thermodynamics",
    natural: "the entropy of an isolated system increases over time according to the second law of thermodynamics",
    compressed: "∂S/∂t ≥ 0 (2nd Law)",
    improvement: "Formal notation enforces precise understanding of inequality direction"
  },
  {
    concept: "Quantum Measurement",
    natural: "the Heisenberg uncertainty principle states that position and momentum cannot both be precisely determined simultaneously",
    compressed: "Δx·Δp ≥ ℏ/2",
    improvement: "Mathematical form reveals it's a fundamental limit, not measurement error"
  },
  {
    concept: "Gibbs Free Energy",
    natural: "a chemical reaction is spontaneous if Gibbs free energy change is negative",
    compressed: "ΔG < 0 ⟹ spontaneous",
    improvement: "Formal logic clarifies necessary and sufficient conditions"
  },
  {
    concept: "Chemical Equilibrium",
    natural: "at equilibrium the forward and reverse reaction rates are equal and the equilibrium constant relates to free energy",
    compressed: "K = e^(-ΔG°/RT)",
    improvement: "Exponential relationship made explicit"
  },
  {
    concept: "Distributed Consensus",
    natural: "a Byzantine fault tolerant system can function correctly if less than one third of nodes are faulty",
    compressed: "BFT: correct iff f < n/3",
    improvement: "Precise threshold made explicit, no ambiguity"
  }
];

console.log("How Formal Notation Improves Reasoning:\n");
for (const item of reasoningImprovements) {
  const naturalTokens = enc.encode(item.natural).length;
  const compressedTokens = enc.encode(item.compressed).length;
  console.log(`**${item.concept}**`);
  console.log(`  Natural: ${item.natural}`);
  console.log(`  Compressed: ${item.compressed}`);
  console.log(`  Tokens: ${naturalTokens} → ${compressedTokens} (${naturalTokens - compressedTokens > 0 ? 'saves' : 'adds'} ${Math.abs(naturalTokens - compressedTokens)})`);
  console.log(`  Reasoning benefit: ${item.improvement}\n`);
}

const annualSavingsExample = savingsPerPaper * 1000 * 365;

console.log("=== SUMMARY ===\n");
console.log(`Chemistry compression alone: ${((chemTotalNatural - chemTotalCompressed)/chemTotalNatural*100).toFixed(1)}% savings`);
console.log(`Total per paper (reasoning + output): ${(totalSavings/totalTokensWithoutCompression*100).toFixed(1)}% savings`);
console.log(`Annual savings at 1000 papers/day: $${annualSavingsExample}`);