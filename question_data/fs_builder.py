"""
question_data/fs_builder.py
Generates forensic science interview questions fs_3 to fs_100 (98 questions).
Combined with fs_1 and fs_2 in questions.json, yields exactly 100 questions.
"""

def get_fs_questions():
    questions_raw = [
        # --- Forensic Biology & DNA (fs_3 to fs_20) ---
        (
            3,
            "Explain how Short Tandem Repeat (STR) analysis works in human identification and why tetranucleotide repeats are preferred.",
            "Medium",
            ["str", "short tandem repeat", "tetranucleotide", "codis", "amplification", "electrophoresis"],
            "Highlight repeat units (3-5 bp), low stutter, high polymorphism, and standard PCR amplification.",
            "STR analysis evaluates specific polymorphic loci where 2-6 base pair sequences repeat consecutively. Tetranucleotide repeats (4 bp) are preferred because they provide high discrimination power while minimizing PCR stutter artifacts compared to dinucleotides. Multiplex PCR amplifies 20+ core CODIS STR loci simultaneously, followed by capillary electrophoresis with fluorescent dye labeling to separate alleles by size. Calculating match probabilities across independent loci using Hardy-Weinberg equilibrium yields random match probabilities exceeding 1 in trillions."
        ),
        (
            4,
            "How does differential extraction separate male sperm DNA from female epithelial DNA in sexual assault evidence?",
            "Hard",
            ["differential extraction", "sperm", "epithelial", "dtt", "proteinase k", "sexual assault"],
            "Describe the two-step lysis mechanism using proteinase K alone, then proteinase K plus DTT (dithiothreitol).",
            "Differential extraction exploits structural differences in cell membranes. First, epithelial cells are lysed using mild digestion with Proteinase K and SDS detergent, leaving sperm nuclei intact due to their disulfide-crosslinked nuclear membranes. Centrifugation pellets the intact sperm, and the supernatant (female fraction) is removed. The pellet is washed extensively, then lysed using Proteinase K combined with DTT (dithiothreitol), which breaks disulfide bonds in sperm protamines (male fraction). This yields two distinct DNA profiles, preventing female epithelial overwhelm of the perpetrator's profile."
        ),
        (
            5,
            "What is Touch DNA (Trace DNA), and what are the primary challenges regarding secondary transfer and low template copy number?",
            "Hard",
            ["touch dna", "low copy number", "secondary transfer", "lcn", "shedder status", "stochastic"],
            "Address stochastic effects (allelic drop-out, drop-in, peak imbalance) and transfer mechanisms.",
            "Touch DNA refers to cellular material transferred from skin friction ridges onto handled objects (often <100 picograms). Challenges include Low Copy Number (LCN) stochastic effects during PCR—such as allelic drop-out (alleles failing to amplify), allelic drop-in (sporadic contamination peaks), and extreme peak height imbalance. Furthermore, secondary and tertiary transfer (A touches B, B touches C) complicates source attribution, as variable individual shedder status means high shedders can leave detectable DNA on items they never directly contacted."
        ),
        (
            6,
            "Compare mitochondrial DNA (mtDNA) sequencing with nuclear STR profiling: when is mtDNA utilized in forensic cases?",
            "Medium",
            ["mtdna", "mitochondrial dna", "maternal lineage", "hvr1", "hvr2", "degraded skeletal"],
            "Note high copy number per cell, maternal inheritance, lack of recombination, and hypervariable regions.",
            "Nuclear STRs provide unique individual identification (except identical twins) but require intact nuclear DNA (~1 copy per cell). In contrast, cells contain hundreds to thousands of mitochondria, yielding high mtDNA copy numbers that survive harsh degradation, such as in charred remains, ancient bones, or shed hair shafts lacking root tissue. Forensic mtDNA targets hypervariable regions HVR-1 and HVR-2. Because mtDNA is inherited maternally without recombination, all maternal relatives share the sequence, meaning it excludes suspects or establishes maternal lineage rather than identifying a single person uniquely."
        ),
        (
            7,
            "Explain the principles and interpretation of Y-STR testing in forensic casework.",
            "Medium",
            ["y-str", "male specific", "haplotype", "paternal lineage", "mixture", "sexual assault"],
            "Focus on male-specific amplification in high female background mixtures and non-recombining portion of the Y chromosome.",
            "Y-STR analysis targets short tandem repeats exclusively on the non-recombining region of the male Y chromosome (NRY). It is invaluable in sexual assault cases where high levels of female epithelial DNA would overwhelm low male donor DNA in standard autosomal STR kits, and in multi-male perpetrator mixtures. Because the NRY lacks recombination, linked Y-STR loci form a haplotype passed paternal lineage intact (barring mutations). It cannot distinguish between patrilineally related males (father, brothers, paternal uncles), so statistics use the haplotype counting method rather than the product rule."
        ),
        (
            8,
            "What is the function of the Kastle-Meyer (phenolphthalein) test, and how do you differentiate true positive from chemical false positives?",
            "Easy",
            ["kastle-meyer", "phenolphthalein", "presumptive test", "hemoglobin", "peroxidase", "false positive"],
            "Explain the two-step addition (KM reagent first, then hydrogen peroxide) to catch chemical oxidants.",
            "The Kastle-Meyer test is a presumptive catalytic color test for blood. Hemoglobin's heme group exhibits peroxidase-like activity, catalyzing the oxidation of reduced colorless phenolphthalin into pink phenolphthalein by hydrogen peroxide. To detect chemical false positives (plant peroxidases or oxidizing minerals like copper/iron salts), the reagents are applied sequentially: first KM reagent alone (it must remain colorless; if it turns pink immediately, a non-heme chemical oxidant is present), followed by 3% hydrogen peroxide. An immediate bright pink reaction after peroxide indicates presumptive blood."
        ),
        (
            9,
            "How does Luminol and Bluestar chemiluminescence detect latent bloodstains, and what substances cause false positive luminescence?",
            "Medium",
            ["luminol", "bluestar", "chemiluminescence", "latent blood", "bleach", "iron catalyst"],
            "Describe heme iron oxidation catalysis producing light at ~425 nm, and mention common false positives like hypochlorite bleach.",
            "Luminol (3-aminophthalhydrazone) and its stabilized commercial form Bluestar react with an oxidant (sodium perborate or hydrogen peroxide) in alkaline conditions. Heme iron in hemoglobin acts as a catalyst, producing excited 3-aminophthalate dianions that emit a characteristic bright blue chemiluminescent glow (~425 nm) upon relaxing to ground state. It is sensitive up to 1:100,000 dilution and works on cleaned crime scenes. Common false positives include household hypochlorite bleach, copper and iron pipes, plant peroxidases (horseradish), and certain paints; bleach produces a fast, fading flash compared to the sustained glow of blood."
        ),
        (
            10,
            "What are confirmatory tests for human blood, and how does the Takayama crystal test work?",
            "Medium",
            ["takayama", "hemochromogen", "confirmatory test", "crystals", "pyridine", "rsid"],
            "Contrast presumptive catalytic tests with microscopic crystal formation (pyridine hemochromogen) or immunochromatographic assays.",
            "While catalytic tests (KM, Luminol) are merely presumptive, confirmatory tests verify blood presence unequivocally. The Takayama (hemochromogen) crystal test involves heating dried stain extract with a reagent containing pyridine, glucose, and sodium hydroxide. Pyridine binds to the ferrous heme iron of denatured hemoglobin, forming salmon-pink, rhomboid crystals of pyridine ferroprotoporphyrin viewed under 400x magnification. Modern laboratories frequently replace microcrystalline tests with rapid immunochromatographic assays (e.g., ABAcard HemaTrace, RSID-Blood) targeting human hemoglobin or glycophorin A antigens."
        ),
        (
            11,
            "Explain how the Acid Phosphatase (AP) test and p30 (PSA) test verify the presence of seminal fluid.",
            "Medium",
            ["acid phosphatase", "p30", "psa", "prostate specific antigen", "semen", "brentamine"],
            "Discuss rapid purple color change with Brentamine Fast Blue and immunochromatographic confirmation with p30.",
            "Seminal fluid screening begins with the Brentamine Fast Blue test for prostatic Acid Phosphatase (AP), an enzyme secreted in massive concentrations by the prostate. AP hydrolyzes alpha-naphthyl phosphate, producing free naphthol that couplers with diazonium dye (Fast Blue B) to produce an intense purple color within 30 seconds. Confirmatory testing is accomplished either by microscopic observation of spermatozoa (Christmas Tree stain) or by immunochromatographic detection of p30 / Prostate Specific Antigen (PSA) or Semenogelin, which confirms semen even in vasectomized or azoospermic males."
        ),
        (
            12,
            "How does Next-Generation Sequencing (NGS) / Massively Parallel Sequencing (MPS) expand forensic casework beyond capillary electrophoresis?",
            "Hard",
            ["ngs", "mps", "massively parallel sequencing", "snp", "phenotyping", "isoalleles"],
            "Discuss sequence-level variations (isoalleles), simultaneous autosomal/Y/mtDNA typing, and forensic DNA phenotyping.",
            "Capillary Electrophoresis (CE) only measures the physical length/size of PCR fragments, grouping different sequences of identical length together. NGS/MPS directly sequences the exact base order of every fragment. This reveals 'isoalleles' (STRs with identical length but distinct internal sequence polymorphisms), vastly increasing statistical discrimination. Furthermore, MPS multiplexes hundreds of markers in a single assay: combining autosomal STRs, Y-STRs, X-STRs, identity SNPs, biogeographical ancestry-informative markers (AIMs), and phenotypic SNPs (hair/eye/skin color prediction), and handles severely degraded DNA with small amplicon sizes."
        ),
        (
            13,
            "What is Forensic Genetic Genealogy (FGG / IGG) and how are SNP microarrays combined with public databases to solve cold cases?",
            "Hard",
            ["fgg", "igg", "forensic genealogy", "gedmatch", "snps", "centi-morgans"],
            "Explain dense SNP arrays (hundreds of thousands of SNPs), shared identity-by-descent (IBD) segments, centiMorgans, and tree building.",
            "Forensic Investigative Genetic Genealogy (FIGG) uses dense SNP microarrays or whole-genome sequencing (profiling 600,000+ single nucleotide polymorphisms) rather than standard 20-locus STRs. The resulting profile is uploaded to consenting genetic genealogy databases (e.g., GEDmatch PRO, FamilyTreeDNA) to identify distant relatives through shared Identity-by-Descent (IBD) DNA segments measured in centiMorgans (cM). Forensic genealogists construct reverse family trees from shared 2nd, 3rd, or 4th cousins back to common ancestral couples, then research descendancy lines cross-referenced with geographic and demographic data to identify candidate suspects."
        ),
        (
            14,
            "Explain PCR inhibition in forensic samples: name three common inhibitors and methods to overcome them.",
            "Medium",
            ["pcr inhibition", "heme", "humic acid", "melanin", "bsa", "dilution"],
            "Identify heme (blood), humic acid (soil), melanin (hair/skin), and remediation techniques (BSA, cleanup columns, dilution).",
            "PCR inhibitors are co-extracted substances that interfere with DNA polymerase activity, magnesium cofactor binding, or primer annealing. Three common environmental inhibitors are: (1) Heme from blood, (2) Humic acid from buried specimens in soil, and (3) Melanin from dark hair and highly pigmented skin. Methods to mitigate inhibition include: adding Bovine Serum Albumin (BSA) to bind and neutralize inhibitors, serial dilution of the template extract (reducing inhibitor concentration below toxic threshold while retaining sufficient template), and using silica-based spin column cleanups or modern engineered polymerases (e.g., AmpliTaq Gold)."
        ),
        (
            15,
            "What is allelic drop-out, and why is it dangerous in forensic DNA mixture interpretation?",
            "Hard",
            ["allelic drop-out", "stochastic threshold", "mixture interpretation", "false exclusion", "heterozygote"],
            "Define amplification failure of one allele in a heterozygote below stochastic threshold and potential for false exclusion.",
            "Allelic drop-out occurs in low-template or degraded DNA when one of two alleles at a heterozygous locus fails to amplify above detection thresholds due to random sampling fluctuations during initial PCR cycles. This causes a true heterozygous genotype (e.g., 14, 16) to falsely appear homozygous (e.g., 14). In mixture interpretation, allelic drop-out can lead analysts to mistakenly exclude a true contributor whose minor allele dropped out, or miscalculate contributor ratios, likelihood ratios, and random match probabilities unless probabilistic genotyping software accounts for drop-out probabilities."
        ),
        (
            16,
            "How does Probabilistic Genotyping (e.g., STRmix, TrueAllele) handle complex forensic DNA mixtures?",
            "Hard",
            ["probabilistic genotyping", "strmix", "trueallele", "mcmc", "likelihood ratio", "continuous model"],
            "Discuss Markov Chain Monte Carlo (MCMC), biological modeling (peak height, stutter, degradation), and Likelihood Ratio (LR).",
            "Traditional binary mixture interpretation applies hard threshold cutoffs (analytical and stochastic), often discarding ambiguous low-level data. Continuous probabilistic genotyping software (STRmix, TrueAllele) uses Markov Chain Monte Carlo (MCMC) algorithms and biological modeling of peak heights, locus-specific stutter ratios, allele drop-out, drop-in, and degradation curves. It simulates millions of genotype combinations to determine probability distributions, calculating a mathematically rigorous Likelihood Ratio (LR) comparing prosecution hypothesis (suspect contributed) against defense hypothesis (unknown unrelated person contributed)."
        ),
        (
            17,
            "How do forensic examiners differentiate human blood from non-human animal blood in casework?",
            "Easy",
            ["precipitin test", "hematrace", "anti-human", "cross-reactivity", "species identification"],
            "Mention the Ouchterlony double diffusion, precipitin ring tests, and mobile immunochromatographic cards like ABAcard HemaTrace.",
            "Species identification is determined using immunological assays based on antigen-antibody precipitation. The classic precipitin test layers extract against anti-human serum; a precipitate ring forms at the interface if human serum albumin/globulin is present. In modern labs, lateral flow immunochromatographic strip tests (e.g., ABAcard HemaTrace) use mobile monoclonal anti-human hemoglobin antibodies that form a visible pink test band. While highly specific to higher primates and humans, cross-reactivity checks with domestic animals (dogs, cats, pigs, cattle) are always validated."
        ),
        (
            18,
            "What is the RSID (Rapid Stain Identification) system, and why is it superior to catalytic tests for saliva detection?",
            "Medium",
            ["rsid", "saliva", "alpha-amylase", "monoclonal antibody", "phadebas", "confirmatory"],
            "Contrast amylase catalytic digestion (Phadebas) with specific monoclonal detection of human salivary alpha-amylase.",
            "Older saliva screening methods (e.g., Phadebas tablet or starch-iodine assays) test for alpha-amylase enzymatic digestion of starch. However, amylase is found in high levels in feces, perspiration, pancreatic secretions, and bacteria, leading to false positives. RSID-Saliva uses dual monoclonal antibodies specific to human salivary alpha-amylase (encoded by the AMY1 gene) rather than pancreatic amylase (AMY2). It operates via lateral flow immunochromatography, producing an antigen-antibody sandwich that eliminates cross-reactivity with other body fluids."
        ),
        (
            19,
            "Describe the extraction and profiling of DNA from bone and tooth samples in forensic anthropology.",
            "Hard",
            ["bone extraction", "tooth", "petrous bone", "total demineralization", "edta", "ancient dna"],
            "Detail cleaning, milling into fine powder, total demineralization with EDTA, and silica-binding extraction.",
            "Dense cortical bone (femur, tibia) and petrous portion of temporal bone, or tooth pulp/cementum, are targeted because mineralized hydroxyapatite shields DNA from environmental degradation. The sample is cleaned with sodium hypochlorite and sanded to remove surface contaminants, then cryogenic freezer-milled into a fine bone powder. Total demineralization uses concentrated 0.5 M EDTA (pH 8.0) over 24-48 hours to chelate calcium ions, releasing trapped osteocytes. Digestion with Proteinase K and extraction via silica-membrane spin columns or magnetic beads purifies high-quality DNA."
        ),
        (
            20,
            "What is the CODIS database structure in the United States, and what are its three operational tiers?",
            "Easy",
            ["codis", "ndis", "sdis", "ldis", "offender index", "forensic index"],
            "List LDIS (Local), SDIS (State), and NDIS (National), and contrast the Forensic Unknown Index with Convicted Offender Index.",
            "CODIS (Combined DNA Index System) operates on three hierarchical levels: LDIS (Local DNA Index System at municipal/county crime labs), SDIS (State DNA Index System), and NDIS (National DNA Index System managed by the FBI). CODIS contains distinct indexes, most notably: (1) Forensic Index containing unknown DNA profiles recovered from crime scenes, and (2) Convicted Offender and Arrestee Index containing reference profiles from convicted felons and qualifying arrestees. Matches link unsolved crime scenes together or identify known perpetrators."
        ),

        # --- Forensic Toxicology & Chemistry (fs_21 to fs_40) ---
        (
            21,
            "Explain the working principles of Gas Chromatography-Mass Spectrometry (GC-MS) in forensic drug confirmation.",
            "Medium",
            ["gc-ms", "gas chromatography", "mass spectrometry", "electron ionization", "mass spectrum", "retention time"],
            "Explain mobile carrier gas, capillary column separation by volatility/polarity, 70 eV electron ionization, and spectral fingerprinting.",
            "GC-MS is the gold-standard confirmatory tool for volatile and semi-volatile drugs. The GC separates mixture components: an inert carrier gas (helium) carries vaporized analytes through a fused silica capillary column where compounds partition between the gas and stationary phase based on boiling point and polarity, eluting at characteristic retention times. Molecules then enter the mass spectrometer ion source, undergoing Electron Ionization (typically 70 eV), which fragments molecules into characteristic cation fragments. A quadrupole mass analyzer filters ions by mass-to-charge ratio (m/z), producing a reproducible fragmentation spectrum matched against reference libraries."
        ),
        (
            22,
            "How does Liquid Chromatography-Tandem Mass Spectrometry (LC-MS/MS) differ from GC-MS, and why is it preferred for fentanyl analogs and thermally labile toxins?",
            "Hard",
            ["lc-ms/ms", "tandem mass spectrometry", "electrospray ionization", "fentanyl", "thermally labile", "derivatization"],
            "Highlight no need for high heat or chemical derivatization, soft electrospray ionization (ESI), and MRM sensitivity.",
            "GC-MS requires analytes to be vaporized at 250-300°C without decomposing; polar or thermally labile molecules must undergo tedious chemical derivatization (e.g., silylation). LC-MS/MS separates liquid analytes at room or moderate temperature using high-pressure liquid chromatography, followed by atmospheric pressure soft ionization (Electrospray Ionization, ESI). Tandem MS (MS/MS) uses collision-induced dissociation (CID) in Multiple Reaction Monitoring (MRM) mode to isolate a precursor ion and detect specific product ion transitions, delivering femtogram-level sensitivity critical for trace potent synthetic opioids (fentanyl, carfentanil)."
        ),
        (
            23,
            "Explain how Headspace Gas Chromatography with Flame Ionization Detection (HS-GC-FID) quantifies Blood Alcohol Concentration (BAC).",
            "Medium",
            ["headspace gc", "blood alcohol concentration", "bac", "henry's law", "flame ionization", "ethanol"],
            "Mention Henry's Law of gas-liquid equilibrium in sealed vials, dual-column confirmation, and internal standard (n-propanol).",
            "HS-GC-FID measures volatile ethanol in whole blood without injecting messy biological fluids onto columns. Whole blood is mixed with an internal standard (n-propanol) in a hermetically sealed vial and thermostatted at 60-70°C. According to Henry's Law, the vapor pressure of ethanol in the headspace gas is directly proportional to its concentration in the liquid phase at equilibrium. Headspace gas is automatically sampled and injected across dual capillary columns with different polarities connected to Flame Ionization Detectors (FID), providing simultaneous quantitation and dual-column confirmation."
        ),
        (
            24,
            "What is postmortem redistribution (PMR), and why is femoral blood preferred over cardiac blood for toxicological quantification?",
            "Hard",
            ["postmortem redistribution", "pmr", "femoral blood", "cardiac blood", "diffusion", "site dependence"],
            "Explain passive postmortem drug diffusion from high-concentration organs (liver, lungs, myocardium) into heart chambers.",
            "Postmortem redistribution (PMR) is the time-dependent, passive diffusion of drugs from reservoir organs of high drug concentration (e.g., liver, lungs, myocardium, stomach contents) into adjacent vascular compartments and heart blood after death. Basic, highly lipophilic drugs with large volumes of distribution (e.g., tricyclic antidepressants, digoxin, methamphetamine) exhibit marked PMR, causing heart blood concentrations to appear artificially elevated compared to antemortem levels. Femoral blood, drawn from the peripheral femoral vein after ligating it, is isolated from central organ diffusion and reflects true circulating antemortem blood levels."
        ),
        (
            25,
            "Why is vitreous humor an invaluable specimen in forensic toxicology and postmortem biochemistry?",
            "Medium",
            ["vitreous humor", "postmortem interval", "potassium", "electrolytes", "glucose", "putrefaction"],
            "Note anatomical isolation, resistance to putrefaction, potassium levels for PMI, and glucose/lactate for diabetic ketoacidosis.",
            "Vitreous humor, the gelatinous fluid filling the eye posterior chamber, is anatomically protected within the bony orbit and blood-retina barrier, making it relatively immune to postmortem microbial contamination, putrefaction, and postmortem redistribution. It is the premier specimen for confirming ethanol intake (differentiating antemortem consumption from postmortem microbial fermentation), evaluating diabetic ketoacidosis (glucose and beta-hydroxybutyrate), renal failure (urea nitrogen and creatinine), and estimating Postmortem Interval (PMI) via linear rise in vitreous potassium."
        ),
        (
            26,
            "How does carbon monoxide poisoning cause death, and how is carboxyhemoglobin (COHb) measured in postmortem blood?",
            "Medium",
            ["carbon monoxide", "carboxyhemoglobin", "cohb", "co-oximetry", "cherry red", "hypoxia"],
            "Explain 200x higher affinity for hemoglobin than oxygen, shift of oxygen dissociation curve, cherry-red lividity, and spectrophotometric CO-oximetry.",
            "Carbon monoxide (CO) binds to hemoglobin with an affinity ~200-250 times greater than oxygen, forming carboxyhemoglobin (COHb). This blocks oxygen binding and induces an allosteric conformational shift that locks remaining oxygen onto hemoglobin, inhibiting oxygen release into tissues and causing cellular histotoxic hypoxia. Gross findings reveal characteristic cherry-red postmortem lividity and organ coloration. In the laboratory, COHb saturation percentage is measured quantitatively via automated multi-wavelength spectrophotometry (CO-oximetry) or by releasing CO gas with sulfuric acid and analyzing via GC-TCD."
        ),
        (
            27,
            "Explain the mechanism of cyanide toxicity and the analytical method for detecting cyanide in forensic autopsy samples.",
            "Hard",
            ["cyanide", "cytochrome c oxidase", "histotoxic hypoxia", "microdiffusion", "bitter almonds", "colorimetry"],
            "Detail inhibition of cytochrome c oxidase in mitochondrial electron transport, Conway microdiffusion, and colorimetric pyridine-barbituric acid detection.",
            "Cyanide binds with high affinity to the ferric (Fe3+) ion in cytochrome c oxidase (complex IV) of the mitochondrial electron transport chain. This arrests oxidative phosphorylation and halts ATP synthesis; cells cannot utilize available oxygen, causing rapid lethal cellular hypoxia with elevated venous oxygen saturation (bright pink blood). Postmortem detection involves Conway microdiffusion: whole blood is acidified in a closed chamber to volatilize hydrogen cyanide gas, which is trapped in sodium hydroxide and quantified via spectrophotometry (pyridine-barbituric acid reaction) or headspace GC-NPD/MS."
        ),
        (
            28,
            "How do screening immunoassay techniques (ELISA, EMIT) work in forensic urine and blood drug screening?",
            "Easy",
            ["elisa", "emit", "immunoassay", "competitive binding", "presumptive drug screen", "cross-reactivity"],
            "Explain competitive antibody binding between labeled drug and unlabeled sample drug, optical density cutoff, and presumptive status.",
            "Screening immunoassays utilize competitive antigen-antibody binding. A fixed quantity of enzyme-labeled drug (conjugate) and the biological sample compete for a limited number of drug-specific antibody binding sites coated on a microplate (ELISA) or in homogeneous solution (EMIT). Higher drug concentration in the sample leaves fewer binding sites for the enzyme-labeled conjugate, modulating substrate enzymatic conversion and optical absorbance. Immunoassays are high-throughput but purely presumptive due to class cross-reactivity and matrix interference, requiring GC-MS or LC-MS/MS confirmation."
        ),
        (
            29,
            "Explain the difference between therapeutic, toxic, and lethal drug concentrations in forensic toxicology interpretation.",
            "Medium",
            ["therapeutic", "toxic", "lethal", "pharmacodynamics", "tolerance", "drug-drug interactions"],
            "Discuss overlap, individual tolerance (e.g. chronic opioid users), pharmacogenomic variations, and polydrug synergy.",
            "In forensic toxicology, concentration numbers cannot be interpreted in a vacuum. A 'therapeutic' range produces desired medical effects; 'toxic' concentrations induce physiological impairment and organ damage; 'lethal' concentrations directly cause fatal circulatory or respiratory collapse. However, significant overlap occurs: an opioid concentration lethal to an opioid-naive individual may be therapeutic or well-tolerated in a chronic pain patient due to pharmacological tolerance. Analysts must evaluate full autopsy context, drug-drug synergistic interactions (e.g., benzodiazepine + opioid CNS depression), active metabolites, and decedent medical history."
        ),
        (
            30,
            "How are heavy metal poisons (arsenic, thallium, lead, mercury) detected in biological matrices using ICP-MS?",
            "Hard",
            ["icp-ms", "inductively coupled plasma", "heavy metals", "arsenic", "thallium", "acid digestion"],
            "Discuss argon plasma atomization/ionization at 10,000 K, quadrupole mass filtering, and microwave acid digestion.",
            "Biological tissues (liver, kidney, hair, bone) undergo closed-vessel microwave-assisted acid digestion with concentrated nitric acid and hydrogen peroxide to break down organic matrices. The clarified aqueous solution is introduced into Inductively Coupled Plasma Mass Spectrometry (ICP-MS). An argon gas plasma heated to 8,000–10,000 Kelvin completely atomizes the sample and strips electrons to generate positive elemental ions. These ions are extracted into high vacuum and filtered by mass-to-charge ratio via quadrupole or sector-field mass analyzer, detecting trace metals down to parts-per-trillion (ppt) levels."
        ),
        (
            31,
            "What is segmental hair analysis in forensic toxicology, and how is it used to document chronological drug exposure?",
            "Medium",
            ["hair analysis", "segmental analysis", "growth rate", "chronological exposure", "decontamination"],
            "Mention hair growth rate ~1 cm/month, wash decontamination procedures to exclude external deposition, and historical dosing.",
            "Scalp hair grows at an average rate of approximately 1 cm per month. As hair shafts keratinize, circulating drugs and metabolites from capillary blood diffuse into the hair follicle matrix and become permanently trapped inside the cortex. By cutting hair bundles into 1-cm segments from proximal root to distal tip and analyzing each section via LC-MS/MS, toxicologists reconstruct a monthly timeline of substance exposure or poisoning (e.g., chronic heavy metal administration). Rigorous organic washing protocols are mandatory to eliminate external environmental contamination."
        ),
        (
            32,
            "What is the difference between free morphine, codeine, and 6-monoacetylmorphine (6-MAM) in proving heroin exposure?",
            "Medium",
            ["6-mam", "heroin", "morphine", "codeine", "diacetylmorphine", "metabolism"],
            "Emphasize 6-MAM as the definitive biomarker that proves heroin use, as heroin rapidly hydrolyzes to 6-MAM then morphine.",
            "Heroin (diacetylmorphine) has a half-life of only 2 to 6 minutes in blood, rapidly deacetylating into 6-monoacetylmorphine (6-MAM), which subsequently hydrolyzes to morphine (half-life 2-3 hours). Because morphine can originate from prescription morphine, codeine metabolism, or poppy seed consumption, morphine alone does not establish heroin ingestion. The detection of 6-monoacetylmorphine (6-MAM) in blood, urine, or vitreous humor provides indisputable proof of illicit heroin intake, as 6-MAM is unique to the synthetic diacetylation pathway of morphine."
        ),
        (
            33,
            "How does microbial ethanol production occur in decomposing bodies, and how do forensic toxicologists differentiate it from antemortem drinking?",
            "Hard",
            ["microbial ethanol", "neoformation", "putrefaction", "n-propanol", "vitreous humor", "ethyl glucuronide"],
            "Discuss Candida albicans / bacterial glucose fermentation, testing vitreous humor/urine, and biomarkers like ethyl glucuronide (EtG).",
            "During decomposition, postmortem microbial proliferation (e.g., Candida albicans, Enterobacter cloacae) ferments endogenous glucose and amino acids into ethanol (neoformation), sometimes reaching levels >0.10 g/dL. Toxicologists differentiate postmortem synthesis from true antemortem consumption by: (1) Testing isolated compartments lacking microbes or glucose, notably vitreous humor and sealed bladder urine; (2) Monitoring concomitant microbial volatiles like n-propanol, isopropanol, and acetaldehyde; and (3) Testing for non-oxidative direct ethanol metabolites, Ethyl Glucuronide (EtG) and Ethyl Sulfate (EtS), which require active liver enzymes and cannot be synthesized postmortem."
        ),
        (
            34,
            "Explain the analytical workflow for extracting unknown organic poisons from whole blood using Solid Phase Extraction (SPE).",
            "Medium",
            ["solid phase extraction", "spe", "conditioning", "washing", "elution", "sorbent"],
            "Outline four steps: column conditioning, sample loading, selective washing of matrix interferences, and analyte elution.",
            "Solid Phase Extraction (SPE) isolates and purifies drugs from whole blood proteins and lipids. The cartridge contains bonded silica or polymer sorbent (e.g., mixed-mode cation exchange). The workflow consists of four stages: (1) Conditioning/Equilibration: solvating sorbent chains with methanol and buffer; (2) Sample Loading: buffered, centrifuged blood is drawn through, allowing target drugs to bind via hydrophobic and ionic interactions; (3) Washing: solvents (water, weak acids) wash away unwanted salts, proteins, and pigments without disrupting drug binding; (4) Elution: an organic solvent (e.g., ethyl acetate with ammonium hydroxide) disrupts binding to recover clean, concentrated analytes for GC/LC analysis."
        ),
        (
            35,
            "What role does gamma-hydroxybutyrate (GHB) play in drug-facilitated sexual assault (DFSA), and what is the window of detection challenge?",
            "Medium",
            ["ghb", "dfsa", "date rape", "endogenous", "rapid elimination", "cut-off threshold"],
            "Discuss rapid metabolism (half-life ~30 min, urine window <12h), endogenous presence requiring cutoffs, and amnesia effects.",
            "GHB is a potent central nervous system depressant and GABAB receptor agonist that induces rapid drowsiness, disinhibition, sedation, and anterograde amnesia, making it a prevalent drug in drug-facilitated crimes. A primary forensic challenge is its rapid pharmacokinetics: GHB has a half-life of 20-40 minutes and is virtually eliminated within 6-8 hours in blood and 10-12 hours in urine. Furthermore, GHB is an endogenous neurochemical metabolite, so laboratories must apply strict baseline cut-off concentrations (e.g., >5 ug/mL in blood, >10 ug/mL in urine) to differentiate exogenous administration from natural physiological levels."
        ),
        (
            36,
            "How do color spot tests (Marquis, Cobalt Thiocyanate, Duquenois-Levine) screen illicit seized drugs in the field?",
            "Easy",
            ["marquis", "cobalt thiocyanate", "duquenois-levine", "presumptive color test", "cocaine", "marijuana"],
            "Marquis (purple for opiates, orange-brown for amphetamines), Cobalt Thiocyanate (blue for cocaine), Duquenois-Levine (purple organic layer for THC).",
            "Presumptive field color tests involve reacting a minute drug scrap with chemical reagents to generate rapid diagnostic color complexes. The Marquis test (formaldehyde and sulfuric acid) turns deep purple with opiates/heroin and orange-to-brown with amphetamine/methamphetamine. Cobalt Thiocyanate forms a bright blue precipitate in the presence of cocaine base or HCl. The Duquenois-Levine test for cannabis reacts with vanillin and acetaldehyde, followed by chloroform addition; a purple hue separating into the bottom chloroform layer indicates presumptive tetrahydrocannabinol (THC)."
        ),
        (
            37,
            "Explain the difference between gas chromatography detectors: FID, TCD, NPD, and Mass Spectrometry.",
            "Hard",
            ["fid", "tcd", "npd", "detector", "thermal conductivity", "nitrogen phosphorus"],
            "FID (hydrocarbons, flame ionization), TCD (universal thermal conductivity), NPD (nitrogen/phosphorus selectivity), MS (structural identification).",
            "In GC analysis, detectors differ in selectivity and destructive nature: (1) Flame Ionization Detector (FID): burns organic carbon in a hydrogen-air flame to generate ions measured by an electrometer; sensitive and linear for hydrocarbons, destroys sample. (2) Thermal Conductivity Detector (TCD): non-destructive universal detector measuring changes in wire heat dissipation caused by analyte vs carrier gas; ideal for fixed gases (CO). (3) Nitrogen-Phosphorus Detector (NPD): highly selective for nitrogen- or phosphorus-containing organic drugs (alkaloids, pesticides) using a heated rubidium bead. (4) Mass Spectrometer (MS): universal and confirmatory, measuring fragment mass-to-charge ratios for structure identification."
        ),
        (
            38,
            "What is the pharmacokinetics of ethylene glycol poisoning, and what toxic metabolites cause fatal renal failure?",
            "Medium",
            ["ethylene glycol", "glycolic acid", "oxalic acid", "calcium oxalate", "anion gap", "antifreeze"],
            "Discuss metabolism via alcohol dehydrogenase to glycolic acid (metabolic acidosis) and oxalic acid (calcium oxalate monohydrate crystals).",
            "Ethylene glycol (automotive antifreeze) itself is minimally toxic, but is oxidized by hepatic alcohol dehydrogenase into toxic metabolites: glycoaldehyde, glycolic acid, glyoxylic acid, and oxalic acid. Glycolic acid accumulation causes severe high-anion-gap metabolic acidosis. Oxalic acid binds circulating calcium ions, precipitating insoluble calcium oxalate monohydrate crystals in renal proximal tubules, causing acute tubular necrosis, flank pain, and anuric renal failure. Postmortem histology confirms polarization birefringent needle-shaped crystals within kidney tubules."
        ),
        (
            39,
            "How are volatile organic inhalants (butane, propane, toluene) analyzed in fatal huffing cases?",
            "Medium",
            ["inhalants", "volatile solvents", "headspace gc-ms", "toluene", "cardiac arrhythmia", "cryogenic"],
            "Discuss hermetically sealed tissue containers, cryogenic headspace extraction, and 'sudden sniffing death' via myocardial sensitization.",
            "Volatile inhalants (e.g., aerosol propellant butane/propane, glue solvent toluene) induce euphoria followed by 'sudden sniffing death' syndrome due to hydrocarbon-induced sensitization of the myocardium to endogenous catecholamines, triggering lethal ventricular fibrillation. Because volatiles escape rapidly, lung tissue, brain tissue, and blood must be collected in airtight glass containers with minimal headspace. Analysis uses cryogenic or temperature-controlled Headspace GC-MS or SPME (Solid-Phase Microextraction) with low-temperature initial oven programming to retain low-boiling-point volatiles."
        ),
        (
            40,
            "How does toxicological analysis assess the degree of burn mortality versus pre-burn death in fire fatalities?",
            "Medium",
            ["fire death", "carbon monoxide", "carboxyhemoglobin", "soot", "hydrogen cyanide", "antemortem vs postmortem"],
            "Contrast presence of airway soot, high carboxyhemoglobin (>50%), and cyanide from smoke inhalation with clean airways and low COHb.",
            "To prove a victim was alive and breathing during a fire rather than murdered and burned postmortem, toxicologists and pathologists evaluate smoke inhalation biomarkers. Victims alive during active combustion inhale smoke containing carbon monoxide and hydrogen cyanide (from burned synthetic polyurethanes/plastics), producing elevated blood carboxyhemoglobin (often >40–60%) and blood cyanide (>1 mg/L), accompanied by soot coating deep trachea and bronchial bifurcations. If the individual died before the fire, carboxyhemoglobin remains normal (<5-10%) and lower airways remain soot-free."
        ),

        # --- Forensic Ballistics & Firearms (fs_41 to fs_55) ---
        (
            41,
            "Explain the difference between class characteristics and individual characteristics in forensic firearms identification.",
            "Easy",
            ["class characteristics", "individual characteristics", "caliber", "lands and grooves", "striations", "firearms"],
            "Class: caliber, number and direction of rifling twists (e.g., 6 Right), land/groove width. Individual: unique microscopic striations/imperfections.",
            "Class characteristics are intentional design parameters specified by the manufacturer prior to production. For firearms and fired bullets, these include caliber, number of lands and grooves, direction of rifling twist (e.g., right-hand or left-hand), and widths of lands and grooves. Individual characteristics are unique, microscopic random imperfections, scratches, and machining tool marks produced during broach rifling, barrel reaming, and operational wear. These striations (striae) are unique to a single firearm barrel, enabling positive identification via comparison microscopy."
        ),
        (
            42,
            "How does a comparison microscope confirm that a spent cartridge casing was fired from a specific firearm?",
            "Medium",
            ["comparison microscope", "cartridge casing", "breech face marks", "firing pin impression", "ejector", "extractor"],
            "Discuss side-by-side split screen view, matching breech face striae, firing pin drag/aperture shear, and extractor/ejector marks.",
            "A comparison microscope bridges two optical light microscope paths into a single split-view ocular bridge, allowing side-by-side alignment of an evidence cartridge casing and a test-fired casing. Examiners inspect multiple individual mark types: (1) Firing pin impressions and firing pin drag marks; (2) Breech face marks transferred when Newton's third law drives the casing base back against the breech block under high pressure; and (3) Extractor claw marks and ejector pin gouges. Consistent alignment of unique microscopic striations across multiple regions confirms a common source."
        ),
        (
            43,
            "Explain how Scanning Electron Microscopy with Energy Dispersive X-ray Spectroscopy (SEM-EDX) identifies Gunshot Residue (GSR).",
            "Hard",
            ["sem-edx", "gunshot residue", "gsr", "lead", "barium", "antimony", "characteristic particle"],
            "Detail morphology (spherical condensed droplets) and simultaneous elemental triad: Lead (Pb), Barium (Ba), and Antimony (Sb).",
            "Primer mixtures contain lead styphnate (initiator), barium nitrate (oxidizer), and antimony sulfide (fuel). When struck by the firing pin, extreme heat (1500°C) and pressure vaporize these metals into a plume that rapidly cools into micro-spherical condensed particulate matter. Adhesive stubs dabbed on a shooter's hands are examined via automated SEM-EDX. The SEM locates particles based on high backscattered electron brightness and spherical morphology (0.5 to 5.0 micrometers), while EDX confirms the simultaneous, fused elemental triad of Lead (Pb), Barium (Ba), and Antimony (Sb) inside a single particle."
        ),
        (
            44,
            "How do forensic examiners determine muzzle-to-target distance from gunshot powder patterns on clothing?",
            "Medium",
            ["muzzle-to-target distance", "gunpowder stippling", "sodium rhodizonate", "modified griess test", "soot", "contact wound"],
            "Discuss contact vs close range (soot and burning), intermediate range (powder stippling/tattooing), and chemical visualization tests.",
            "Distance determination correlates gunshot residue spread with firearm discharge distance. Contact wounds display muzzle imprints, fabric tearing (stellate tears), and intense soot lining the bullet hole margins. Intermediate distance (a few inches up to 3-4 feet) deposits unburned and partially burned powder grains, causing skin stippling/tattooing and powder scatter on fabric. Chemical testing visualizes invisible residues: the Modified Griess Test detects nitrites from burned smokeless powder as orange azo dye, while the Sodium Rhodizonate Test detects vaporized lead as purple/blue complexes. Comparing test-fire patterns at calibrated distances brackets the true range."
        ),
        (
            45,
            "What is the National Integrated Ballistic Information Network (NIBIN) and how does the IBIS system operate?",
            "Easy",
            ["nibin", "ibis", "ballistics database", "brass-trax", "bullet-trax", "correlation score"],
            "Discuss automated 3D optical surface scanning of breech face and firing pin marks, algorithmic correlation, and examiner verification.",
            "NIBIN (National Integrated Ballistic Information Network) is an automated database system operated by the ATF that captures digital 2D and 3D topographic images of ballistic evidence. Crime labs use IBIS (Integrated Ballistics Identification System) hardware—specifically BrassTRAX for cartridge casings and BulletTRAX for fired bullets—to scan breech face marks, firing pin impressions, and rifling land engraving. The system calculates mathematical correlation scores ranking the most likely matches against regional and national database entries, alerting firearms examiners to conduct physical comparison microscopy confirmation."
        ),
        (
            46,
            "Explain how chemical acid etching restores obliterated serial numbers on firearms.",
            "Medium",
            ["serial number restoration", "acid etching", "fry's reagent", "plastic deformation", "crystal lattice", "magnetism"],
            "Explain cold stamping plastic deformation beneath visible indentations, altered chemical potential/solubility, and Fry's reagent.",
            "When serial numbers are stamped onto a metal firearm frame with steel dies, the compression strains the metallic crystalline lattice deep beneath the visible stamp (plastic deformation), altering its density, hardness, and chemical reactivity. Even when perpetrators grind off the surface until smooth, the compressed subterranean lattice remains. Forensic examiners polish the ground surface to a mirror finish, then apply acidic etchants (e.g., Fry's reagent for steel: cupric chloride, hydrochloric acid, and water). The strained, energized crystal lattice dissolves faster than the unstrained metal, temporarily revealing the numbers as frosted outlines."
        ),
        (
            47,
            "How is bullet trajectory reconstructed at a crime scene using trajectory rods, lasers, and trigonometric angle calculations?",
            "Medium",
            ["bullet trajectory", "trajectory rods", "lasers", "elliptical defect", "angle of impact", "azimuth"],
            "Discuss collinear penetration points, angle of impact calculations (sin theta = minor/major axis), inclinometers, and laser photography.",
            "Trajectory reconstruction establishes the flight path of a projectile. When a bullet penetrates two or more collinear intermediate surfaces (e.g., car window then car seat, or drywall and interior stud), rigid trajectory rods are inserted through the aligned holes and extended with laser pointers in darkened rooms to photograph straight-line flight paths back to shooter origin zones. For single elliptical ricochet or impact marks, the vertical impact angle is calculated trigonometrically via arcsine of the minor axis divided by major axis (sin theta = width / length), verified with an inclinometer and digital protractor."
        ),
        (
            48,
            "What causes bullet yaw, tumbling, and cavitation inside human tissue in wound ballistics?",
            "Hard",
            ["wound ballistics", "yaw", "tumbling", "temporary cavity", "permanent cavity", "hydrostatic shock"],
            "Contrast temporary cavity (tissue displacement from kinetic energy) and permanent cavity, and explain center-of-gravity aerodynamic destabilization.",
            "In wound ballistics, a bullet's center of mass lies behind its aerodynamic center of pressure. When traversing dense fluid media (human tissue), drag forces overcome rotational gyroscopic stabilization, causing the projectile to angle off its flight axis (yaw) and rotate end-over-end (tumbling). Tumbling dramatically increases the presented frontal surface area, maximizing kinetic energy transfer (KE = 1/2 m v^2). This forms two wound components: (1) The permanent cavity (direct physical tissue crush along the path), and (2) The temporary cavity (radial stretch cavitation driven by hydraulic shock waves tearing elastic tissues)."
        ),
        (
            49,
            "How do examiners differentiate between an entrance bullet wound and an exit bullet wound on human skin?",
            "Medium",
            ["entrance wound", "exit wound", "abrasion collar", "stellate laceration", "beveling", "soot"],
            "Entrance: abrasion ring/collar, soot/stippling, inward inverted margins. Exit: irregular slit/stellate laceration, everted edges, no abrasion ring.",
            "Entrance wounds typically exhibit an 'abrasion collar' or 'abrasion ring'—a narrow circumferential zone of rubbed, denuded epidermis produced as the spinning projectile indents and stretches skin prior to perforation—accompanied by a soot ring (bullet wipe) and inverted wound edges. If close range, gunpowder stippling and soot are present. In contrast, exit wounds are typically larger, irregular, slit-like, or stellate with ragged, everted (pushed outward) margins, and notably lack an abrasion ring, bullet wipe, soot, or gunpowder stippling."
        ),
        (
            50,
            "Explain the difference between polygonal rifling (e.g., Glock barrels) and traditional cut land-and-groove rifling.",
            "Medium",
            ["polygonal rifling", "traditional rifling", "glock", "hammer forging", "striation marks", "microscopic comparison"],
            "Traditional has sharp square-edged lands and grooves; polygonal has smooth hills and valleys, yielding subtle striation marks.",
            "Traditional cut or button rifling produces distinct, sharp-shouldered rectangular lands and grooves inside the barrel bore, imparting crisp, deeply etched land impressions and discrete micro-striations onto the copper bullet jacket. In contrast, polygonal rifling (produced by cold rotary hammer forging, common in Glock, Heckler & Koch) features smooth, rounded transitions consisting of alternating hills and valleys (hexagonal or octagonal profile). This improves gas seal and bullet velocity, but makes microscopic bullet comparison significantly more challenging because fired bullets display smooth, rounded impressions with less pronounced individual striae."
        ),
        (
            51,
            "What is internal, external, and terminal ballistics, and what does each discipline investigate?",
            "Easy",
            ["internal ballistics", "external ballistics", "terminal ballistics", "in-bore", "flight path", "target impact"],
            "Internal: events within firearm from primer strike to muzzle exit. External: bullet flight through atmosphere. Terminal: interaction with target.",
            "Firearms ballistics is categorized into three distinct phases: (1) Internal Ballistics investigates mechanical and thermodynamic events occurring inside the firearm, including firing pin strike, primer ignition, propellant burning rate, internal chamber pressure curve, recoil motion, and engraving of rifling as the bullet traverses the barrel. (2) External Ballistics analyzes the projectile's trajectory through the atmosphere from muzzle exit to target, including drag coefficient, gravity drop, wind drift, velocity degradation, and gyroscopic drift. (3) Terminal Ballistics studies the projectile's physical behavior upon impacting the target, including penetration, fragmentation, deformation, and wound profile."
        ),
        (
            52,
            "How does choke in a shotgun barrel influence shot pattern spread at various ranges?",
            "Easy",
            ["shotgun", "choke", "shot spread", "full choke", "cylinder bore", "patterning"],
            "Explain barrel constriction (Cylinder, Improved Cylinder, Modified, Full) and the rule of thumb spread (approx. 1 inch per yard).",
            "A shotgun choke is a deliberate constriction engineered into the muzzle end of the barrel to control the dispersion and density of the pellet shot pattern. Choke settings range from Cylinder bore (zero constriction, widest dispersion for close targets) to Improved Cylinder, Modified, and Full Choke (tightest constriction, holding shot pellets grouped together over long distances). In forensic range determination, a standard rule of thumb for an unchoked 12-gauge shotgun is that the pellet pattern spreads approximately 1 inch per yard of distance traveled, though exact range requires test-firing with the evidence shotgun and ammunition."
        ),
        (
            53,
            "What is bullet wipe and lead splash, and how are they visualized on dark clothing using infrared imaging?",
            "Medium",
            ["bullet wipe", "lead splash", "infrared photography", "visualizing soot", "soot absorption"],
            "Bullet wipe: dark circumferential ring of soot, lubricant, lead transferred to target fibers. Infrared: dyes reflect IR while carbon soot absorbs it.",
            "Bullet wipe is a dark, grease-like ring deposited on target clothing or skin immediately surrounding an entrance hole, composed of soot, burnt propellant residue, lubricant, and metallic lead wiped off the exterior of the spinning bullet. On dark or blood-soaked garments, bullet wipe and surrounding gunpowder soot are invisible to the naked eye. Forensic photography uses reflected Infrared (IR) imaging (700–900 nm): fabric textile dyes and dark organic bloodstains reflect infrared light and appear white or transparent, while carbonaceous soot strongly absorbs IR, appearing stark black."
        ),
        (
            54,
            "How are toolmarks classified into impression (compression) marks, sliding (striated) marks, and cutting marks?",
            "Easy",
            ["toolmarks", "compression marks", "striated marks", "cutting marks", "mikrosil", "casting"],
            "Impression: perpendicular force stamping tool contour. Striated: scraping motion parallel to surface. Cutting: dual shearing/pinching.",
            "Toolmarks are classified into three mechanical categories based on how the tool interacts with the softer receiving substrate: (1) Impression / Compression marks: generated when a tool is pressed perpendicular against a surface without lateral movement (e.g., crowbar prying a door jamb, hammer head dent), reproducing the outline of the tool. (2) Sliding / Striated marks: produced when a tool scrapes laterally across a surface (e.g., pry bar slip, flathead screwdriver scratch), leaving parallel microscopic striation lines. (3) Cutting marks: formed when two opposing blades shear or pinch an object (e.g., bolt cutters through a padlock shackle, wire cutters)."
        ),
        (
            55,
            "What is Mikrosil or AccuTrans, and how are silicone casting materials applied to forensic toolmarks?",
            "Easy",
            ["mikrosil", "accutrans", "silicone casting", "toolmark casting", "non-destructive", "reversal"],
            "Explain 2-component silicone paste that cures without shrinking, replicating minute striations without damaging evidence.",
            "Mikrosil and AccuTrans are high-fidelity, two-component polyaddition silicone elastomeric casting materials specifically formulated for forensic impression and toolmark recovery. When a toolmark is located on an immovable, heavy structure (e.g., safe door, reinforced door frame), examiners cannot transport the metal substrate to the laboratory. Silicone casting putty mixed with a catalyst paste is applied across the cleaned toolmark. It cures into a flexible, highly stable rubber mold with zero shrinkage, capturing micro-striations down to sub-micron resolution for direct comparison under the microscope."
        ),

        # --- Latent Prints & Biometrics (fs_56 to fs_70) ---
        (
            56,
            "Explain the ACE-V methodology in forensic friction ridge (fingerprint) examination.",
            "Medium",
            ["ace-v", "analysis", "comparison", "evaluation", "verification", "blind verification"],
            "Analysis (quality, substrate, distortion), Comparison (side-by-side minutiae), Evaluation (identification, exclusion, inconclusive), Verification (independent peer).",
            "ACE-V is the standardized scientific framework for friction ridge analysis: (1) Analysis: the examiner assesses print clarity, anatomical orientation, substrate matrix, deposition pressure, and distortions to determine if the print is suitable for comparison. (2) Comparison: the unknown latent print is compared side-by-side with an exemplar print across Level 1 (ridge flow/pattern), Level 2 (individual minutiae points: bifurcations, ridge endings, dots), and Level 3 details (ridge pores, edge contours). (3) Evaluation: the examiner formulates a conclusion: Identification (individualization), Exclusion, or Inconclusive. (4) Verification: an independent, qualified examiner conducts a blinded, autonomous evaluation of the conclusion."
        ),
        (
            57,
            "What are the three levels of fingerprint ridge details used in forensic latent print comparisons?",
            "Easy",
            ["level 1 detail", "level 2 detail", "level 3 detail", "friction ridge", "minutiae", "ridge pores"],
            "Level 1: overall pattern flow (arch, loop, whorl) - cannot individualize. Level 2: minutiae points. Level 3: ridge width, pore morphology.",
            "Fingerprint details are grouped into three hierarchical tiers: Level 1 Detail describes overall ridge flow, pattern type (plain arch, tented arch, radial loop, ulnar loop, plain whorl, accidental whorl), and core/delta placement; it can exclude individuals but cannot achieve individualization. Level 2 Detail comprises specific path deviations known as Galton characteristics or minutiae (ridge endings, bifurcations, islands, enclosures, bridges); the spatial arrangement and relationship of Level 2 details provide sufficient specificity for individualization. Level 3 Detail includes intrinsic micro-features: individual ridge width, shape of ridge contours, and precise morphology and spacing of sweat pores."
        ),
        (
            58,
            "How does cyanoacrylate (superglue) fuming develop latent fingerprints on non-porous surfaces?",
            "Medium",
            ["cyanoacrylate", "superglue fuming", "latent prints", "polymerization", "polycyanoacrylate", "non-porous"],
            "Explain heating ethyl/methyl cyanoacrylate, gaseous vapor reacting with moisture/amino acids in sweat to form durable white polycyanoacrylate polymer.",
            "Cyanoacrylate ester (superglue) fuming is the preeminent technique for visualizing latent prints on non-porous substrates (glass, metals, firearms, plastics). Evidence is placed in an enclosed chamber with controlled relative humidity (~70-80%). Heating liquid cyanoacrylate releases gaseous monomer vapors that condense onto the latent fingerprint residue. Catalyzed by trace moisture, amino acids, and fatty acids deposited by friction ridges, the monomer undergoes base-catalyzed anionic polymerization into polycyanoacrylate, creating a durable, hard, three-dimensional white plastic replica of the ridge patterns that can then be dyed with fluorescent stains (rhodamine 6G, RAM)."
        ),
        (
            59,
            "Explain the chemical mechanism of Ninhydrin in developing latent prints on porous paper substrates.",
            "Medium",
            ["ninhydrin", "porous paper", "amino acids", "ruhemann's purple", "latent prints", "heat and humidity"],
            "Discuss reaction with terminal amino acids from eccrine sweat, decarboxylation, and formation of the purple-violet Ruhemann's Purple complex.",
            "Ninhydrin (triketohydrindene hydrate) is the standard chemical developer for porous items such as paper, cardboard, and untreated wood. Latent print deposits contain eccrine sweat containing non-volatile alpha-amino acids that bind tightly to cellulose paper fibers and persist for decades. When treated with ninhydrin in an organic carrier solvent and subjected to heat and controlled humidity, ninhydrin reacts with primary amines via oxidative decarboxylation and deamination. Two ninhydrin molecules condense with the amine nitrogen to form an intense purple-violet chromophore known as Ruhemann's Purple (absorbance peak ~570 nm)."
        ),
        (
            60,
            "What are DFO and 1,2-Indanedione, and why are they superior to Ninhydrin for developing faint prints on paper?",
            "Hard",
            ["dfo", "1 2-indanedione", "fluorescence", "zinc chloride", "alternate light source", "amino acid developer"],
            "Explain higher sensitivity via intense photoluminescence under alternate light sources (ALS), compared to ninhydrin's visible absorbance.",
            "DFO (1,8-diazafluoren-9-one) and 1,2-indanedione are amino-acid-reactive fluorogenic reagents that develop latent prints on porous paper. While ninhydrin relies on colorimetric light absorption (which can be masked by dark paper or colored printing), DFO and 1,2-indanedione produce highly photoluminescent reaction products. When illuminated with an Alternate Light Source (ALS) at 450–530 nm (blue/green light) and viewed through orange/yellow barrier filters, faint prints glow with intense fluorescence. 1,2-indanedione mixed with zinc chloride post-treatment yields exceptional contrast, revealing prints containing up to three times fewer amino acids than ninhydrin requires."
        ),
        (
            61,
            "How does Amido Black and Coomassie Brilliant Blue visualize latent blood prints at crime scenes?",
            "Easy",
            ["amido black", "coomassie blue", "blood prints", "protein stain", "latent print", "acidic fixing"],
            "Explain fixing protein with 5-sulfosalicylic acid or methanol, followed by staining cellular proteins dark blue-black.",
            "Amido Black (Acid Black 1) and Coomassie Brilliant Blue are protein-staining diazo dyes used to develop and enhance patent friction ridge prints deposited in blood. Because blood is water-soluble, the print must first be chemically fixed to the substrate using 5-sulfosalicylic acid or methanol to prevent blood protein dissolution and ridge feathering. The aqueous or methanol-based dye solution is applied; the dye molecules bind electrostatically to positively charged basic amino acids and proteins in the blood, staining the friction ridges an intense dark blue-black with high optical contrast against light backgrounds."
        ),
        (
            62,
            "Explain the difference between patent, plastic, and latent fingerprints found at crime scenes.",
            "Easy",
            ["patent print", "plastic print", "latent print", "visible print", "three dimensional", "perspiration"],
            "Patent: visible 2D print deposited in contaminant (blood, ink, oil). Plastic: 3D impression in soft material (clay, wax). Latent: invisible sweat print.",
            "Friction ridge impressions at crime scenes fall into three categories: (1) Patent (Visible) prints: two-dimensional impressions left when fingers contaminated with a visible foreign substance (blood, wet paint, printer ink, grease, dirt) contact a surface; visible to the unaided eye. (2) Plastic prints: three-dimensional molded impressions pressed into soft, malleable substrates (candle wax, fresh putty, soft soap, thick grease, wet paint); visible and captured by oblique lighting and casting. (3) Latent prints: invisible or barely visible impressions formed by the transfer of natural eccrine perspiration and sebaceous oils; requiring chemical or physical development."
        ),
        (
            63,
            "How does Small Particle Reagent (SPR) develop latent prints on wet or outdoor non-porous surfaces?",
            "Medium",
            ["small particle reagent", "spr", "molybdenum disulfide", "wet surfaces", "lipids", "suspension"],
            "Explain aqueous suspension of insoluble molybdenum disulfide particles coated with surfactant binding to water-insoluble sebaceous fats.",
            "Standard fingerprint powders cannot be applied to wet surfaces because brush friction streaks moisture and destroys delicate ridge outlines. Small Particle Reagent (SPR) is an aqueous suspension of micro-fine insoluble particles (commonly dark gray molybdenum disulfide, MoS2) combined with a commercial surfactant. When sprayed over a wet vehicle exterior, window, or underwater weapon, the surfactant allows the hydrophobic molybdenum disulfide particles to selectively adhere to the water-insoluble lipids and fatty acids in the sebaceous print residue, yielding dark gray friction ridges rinsed clean with distilled water."
        ),
        (
            64,
            "What is the Next Generation Identification (NGI) system, and how has it expanded on legacy IAFIS?",
            "Easy",
            ["ngi", "iafis", "biometric database", "palm prints", "facial recognition", "iris"],
            "Discuss multimodal biometrics: automated palm prints, Advanced Fingerprint Identification Technology (AFIT), iris scanning, and facial recognition.",
            "The FBI's Next Generation Identification (NGI) system replaced the legacy Integrated Automated Fingerprint Identification System (IAFIS). NGI expanded biometric capabilities from 10-print rolled ink cards to a multimodal biometric repository. Key enhancements include: (1) AFIT (Advanced Fingerprint Identification Technology), which increased algorithmic fingerprint matching accuracy from 92% to over 99.6%; (2) National Palm Print System (NPPS), storing millions of palm prints responsible for 30% of crime scene impressions; (3) Facial Recognition and comparison repositories; and (4) Iris recognition technology for rapid mobile identification."
        ),
        (
            65,
            "How does Vacuum Metal Deposition (VMD) recover latent fingerprints from difficult substrates like polyethylene film and thermal paper?",
            "Hard",
            ["vacuum metal deposition", "vmd", "gold and zinc", "thermal paper", "polyethylene", "physical development"],
            "Explain high-vacuum chamber, thermal evaporation of trace gold nuclei, followed by zinc deposition condensing only on bare substrate (negative print).",
            "Vacuum Metal Deposition (VMD) is an ultra-sensitive physical technique used on thermal paper, polymer banknotes, smooth fabrics, and plastic bags where chemical fuming fails. Evidence is placed in a high-vacuum chamber (10^-4 mbar). First, a minuscule layer of metallic gold (a few nanometers) is thermally evaporated from a tungsten filament, forming atomic clusters across the entire substrate. Next, pure zinc is evaporated. Zinc cannot condense on gold clusters poisoned by organic fats in fingerprint ridges; it only condenses on bare gold on unprinted areas. This creates a striking negative image with shiny metallic background and transparent dark ridges."
        ),
        (
            66,
            "Explain the Henry Classification System and how the primary classification fraction is calculated.",
            "Medium",
            ["henry classification", "primary classification", "whorls", "finger values", "fraction", "10-print card"],
            "Explain paired fingers (even over odd), 1 + even values / 1 + odd values, where whorl presence assigns values (16, 8, 4, 2, 1).",
            "The Henry Classification System is a 10-print manual indexing method that groups fingerprint cards into 1,024 primary classes based solely on the presence of whorl patterns. Fingers are paired as numerator (even fingers: 2, 4, 6, 8, 10) over denominator (odd fingers: 1, 3, 5, 7, 9). Value weights are assigned only if a whorl is present: fingers 1-2 score 16, fingers 3-4 score 8, fingers 5-6 score 4, fingers 7-8 score 2, and fingers 9-10 score 1. Loops and arches receive 0. The fraction is computed as: (1 + sum of even values) / (1 + sum of odd values), producing scores ranging from 1/1 (no whorls) to 32/32 (all whorls)."
        ),
        (
            67,
            "How do magnetic fingerprint powders differ from traditional volcanic ash/flake powders during latent print recovery?",
            "Easy",
            ["magnetic powder", "magnetic wand", "latent print dusting", "non-destructive", "brush damage", "iron flakes"],
            "Magnetic wand uses iron powder to form a soft brush of powder itself, eliminating stiff animal hair bristles that scratch delicate ridges.",
            "Traditional fingerprint dusting utilizes animal hair (camel hair, fiberglass, or feather) brushes dipped in fine carbon black or aluminum flake powders. Stiff bristles can easily abrade, scratch, or sweep away fragile latent print deposits. Magnetic powders consist of finely milled magnetic iron particles coated with pigment. When picked up by a magnetized wand (magna-brush), the iron particles align along magnetic field lines, forming a soft 'brush' made of the powder itself. When swept gently across a non-ferrous surface, only the powder touches the latent deposit, virtually eliminating mechanical ridge damage."
        ),
        (
            68,
            "What is the difference between a friction ridge bifurcation, ending ridge, dot, and enclosure?",
            "Easy",
            ["bifurcation", "ending ridge", "dot", "enclosure", "minutiae", "galton details"],
            "Bifurcation: single ridge splitting into two branches. Ending ridge: abrupt termination. Dot: short ridge as long as wide. Enclosure: splits and rejoins.",
            "These are the primary Level 2 Galton minutiae: (1) Ending Ridge: a continuous friction ridge line that abruptly terminates or comes to an end without continuing. (2) Bifurcation: a single friction ridge that divides or forks into two separate divergent branch ridges. (3) Dot (or Island): an isolated, minute ridge unit whose length is approximately equal to its width, appearing as a solitary point between ridges. (4) Enclosure (or Lake): a single friction ridge that bifurcates into two branches, runs parallel for a brief distance, and then rejoins into a single continuing ridge."
        ),
        (
            69,
            "How do environmental factors (temperature, UV light, humidity) degrade latent print residue over time?",
            "Medium",
            ["print degradation", "evaporation", "eccrine perspiration", "sebaceous lipids", "uv degradation", "oxidation"],
            "Water evaporates rapidly (within hours), leaving non-volatile amino acids, salts, and unsaturated fatty acids that oxidize and polymerize.",
            "Latent print residue is composed of 98% water (eccrine sweat) mixed with inorganic salts, amino acids, and sebaceous lipids (squalene, wax esters, free fatty acids). High ambient temperatures and low humidity accelerate rapid water evaporation within hours of deposition. Sunlight and UV radiation induce photo-oxidation and free-radical cross-linking of unsaturated fatty acids and squalene, making them brittle and less reactive to lipid-staining reagents. Inorganic salts and bound amino acids are highly stable, persisting indefinitely unless subjected to rainwater runoff or high humidity that dissolves and feathers the ridges."
        ),
        (
            70,
            "What is the 'Frye standard' versus the 'Daubert standard' in the admissibility of latent print expert testimony?",
            "Medium",
            ["daubert standard", "frye standard", "expert testimony", "general acceptance", "gatekeeper", "error rate"],
            "Frye: general acceptance in the scientific community. Daubert: judge as gatekeeper testing peer review, falsifiability, standards, error rate.",
            "The Frye standard (1923) requires that scientific expert evidence must have gained 'general acceptance' in its particular field to be admissible in court. The Daubert standard (Federal Rule of Evidence 702, established 1993) replaced Frye in federal and many state courts, establishing the trial judge as an active 'gatekeeper'. Daubert evaluates five empirical criteria: (1) Whether the technique can be and has been empirically tested and falsified; (2) Whether it has been subjected to peer review and publication; (3) Known or potential error rates; (4) Existence and maintenance of operational standards; and (5) General acceptance."
        ),

        # --- Forensic Pathology & Medicolegal Death Investigation (fs_71 to fs_85) ---
        (
            71,
            "Explain Algor Mortis, Rigor Mortis, and Livor Mortis, and how they estimate the Postmortem Interval (PMI).",
            "Medium",
            ["algor mortis", "rigor mortis", "livor mortis", "pmi", "postmortem interval", "cooling rate"],
            "Algor: body cooling (~1.5 F/hr). Rigor: ATP depletion locking actin-myosin (starts 2-4h, peak 12h, resolves 36h). Livor: blood settling (fixed 8-12h).",
            "The classic triad of postmortem changes estimates time since death: (1) Algor Mortis is postmortem body cooling. Under temperate conditions, an unclothed body loses approximately 1.5°F (0.8°C) per hour during early postmortem hours, calculated via the Glaister equation. (2) Rigor Mortis is postmortem muscle stiffening caused by cellular ATP depletion, which prevents the uncoupling of actin-myosin cross-bridges. Stiffening begins in small muscles (jaw, eyelids) within 2-4 hours, reaches maximum rigidity across all joints at 12 hours, and dissipates after 24-36 hours due to autolytic proteolysis. (3) Livor Mortis is the reddish-purple settling of intravascular blood into dependent capillaries under gravity; it appears within 30 minutes, becomes blanchable, and becomes permanently 'fixed' after 8-12 hours due to postmortem hemoconcentration and hemolysis."
        ),
        (
            72,
            "How does forensic entomology utilize blow fly (Calliphoridae) succession to determine Minimum Postmortem Interval (PMImin)?",
            "Medium",
            ["forensic entomology", "blow fly", "calliphoridae", "accumulated degree hours", "adh", "larval instar"],
            "Explain oviposition within minutes of death, egg hatching, three larval instars, pupation, and Accumulated Degree Hours (ADH).",
            "Blow flies (Calliphoridae) are the primary initial colonizers, attracted by volatile putrefactive odors (putrescine, cadaverine) within minutes to hours of death. Females lay eggs in moist natural body orifices (eyes, mouth, nose) or traumatic wounds. Development proceeds through predictable life cycle stages: egg -> 1st instar larva -> 2nd instar -> 3rd instar (feeding and post-feeding wandering) -> pupa -> adult fly. Because insect metabolism is poikilothermic (temperature-dependent), forensic entomologists measure ambient crime scene temperatures and calculate Accumulated Degree Hours (ADH) or Degree Days required to reach the oldest collected larval stage, yielding the Minimum Postmortem Interval (PMImin)."
        ),
        (
            73,
            "Differentiate between sharp force trauma injuries: incised wounds, stab wounds, and chop wounds.",
            "Easy",
            ["sharp force trauma", "incised wound", "stab wound", "chop wound", "depth vs length", "weapon characteristics"],
            "Incised: length on skin greater than depth, clean edges, no bridging. Stab: depth greater than surface length. Chop: heavy, sharp weapon with bone notch.",
            "Sharp force trauma is produced by pointed or edged instruments: (1) Incised wounds (cuts): caused by a sharp edge drawn across skin where the wound length on the skin surface is greater than its depth into tissues; characterized by crisp, clean-cut margins without tissue bridging, abrasion, or contusion. (2) Stab wounds: penetrative injuries caused by pointed instruments where the wound depth beneath the skin is significantly greater than its length on the skin surface; track depth approximates blade length and angle. (3) Chop wounds: inflicted by heavy edged weapons (axes, machetes, meat cleavers) producing sharp skin incision accompanied by underlying crushing, contusion, and deep grooving or fracturing of bone."
        ),
        (
            74,
            "Explain the pathological mechanism of petechial hemorrhages in mechanical asphyxia (strangulation, hanging).",
            "Medium",
            ["petechial hemorrhages", "asphyxia", "strangulation", "venous occlusion", "hydrostatic pressure", "conjunctiva"],
            "Detail venous obstruction (jugular veins collapse at ~4-5 kg) while carotid arteries (~15 kg) stay patent, causing capillary rupture.",
            "Petechiae are pinpoint (1-2 mm) capillary hemorrhages observed in conjunctivae, sclera, periorbital skin, and inner oral mucosa. In compressive neck asphyxiation (manual strangulation, ligature strangulation), compression pressures of only 4.5 to 5 kg are sufficient to completely occlude thin-walled, low-pressure jugular veins, blocking blood drainage from the head. However, the thicker, muscular internal carotid arteries remain patent until 15 kg of force is applied, continuing to pump high-pressure arterial blood into facial tissues. The resulting massive cranial venous engorgement ruptures fragile post-capillary venules under extreme hydrostatic backpressure."
        ),
        (
            75,
            "How do forensic anthropologists determine biological sex, ancestry, and stature from human skeletal remains?",
            "Hard",
            ["forensic anthropology", "biological sex", "pelvis", "skull", "femur length", "trotter-gleser"],
            "Sex: pelvic subpubic angle, sciatic notch, skull brow ridges/nuchal crest. Stature: long bone regression (femur/tibia). Ancestry: craniometrics.",
            "Forensic anthropologists construct a biological profile from skeletal remains: (1) Biological Sex: the adult pelvis is most diagnostic; females display a broad U-shaped subpubic angle (>90°), wide greater sciatic notch, and elevated preauricular sulcus to accommodate childbirth, whereas males display a narrow V-shaped angle (<70°); the skull shows male robusticity (prominent supraorbital ridges, mastoid processes, square mental protuberance). (2) Stature: measured maximum lengths of intact long bones (femur, tibia, humerus) are input into population-calibrated mathematical regression equations (e.g., Trotter-Gleser formulas). (3) Ancestry: evaluated via metric 3D craniometrics (Fordisc software) and non-metric cranial midfacial features."
        ),
        (
            76,
            "What is diatom testing in suspected drowning cases, and how does it differentiate true drowning from postmortem body disposal in water?",
            "Hard",
            ["diatom test", "drowning", "diatoms", "pulmonary alveolar capillary", "bone marrow", "postmortem immersion"],
            "Explain inhalation of water with microscopic silica diatoms, alveolar rupture into circulation, lodging in closed organs like femoral bone marrow.",
            "Diatoms are microscopic, unicellular photosynthetic algae with rigid, silica-rich cell walls (frustules) inhabiting natural water bodies. In active antemortem drowning, the victim inhales aspirated water deep into pulmonary alveoli; increasing hydrostatic pressure and alveolar-capillary rupture allow microscopic diatoms (<30 um) to enter the systemic bloodstream and embolize to distant closed organs (femur bone marrow, brain, kidneys, liver). If a dead body is dumped into water postmortem, lack of circulation prevents diatoms from penetrating closed bone marrow. Acid digestion of bone marrow and microscopic recovery of species-matched diatoms confirms antemortem drowning."
        ),
        (
            77,
            "Explain the stages of human decomposition: fresh, bloat, active decay, advanced decay, and dry skeletal remains.",
            "Medium",
            ["decomposition stages", "fresh", "bloat", "active decay", "putrefaction", "skeletonization"],
            "Fresh (autolysis), Bloat (anaerobic gut bacteria produce methane/H2S), Active (purge fluid, maggots, skin slippage), Advanced, Dry remains.",
            "Human decomposition follows five progressive morphological stages: (1) Fresh stage: autolysis begins as intracellular enzymes self-digest cells; algor, rigor, and livor mortis develop without gross odor. (2) Bloat stage: gut anaerobic enteric bacteria (Clostridium) proliferate and metabolize, releasing large volumes of foul-smelling gases (methane, hydrogen sulfide, ammonia), causing abdominal distension, marbling of veins, tongue protrusion, and purulent blood-tinged purge fluid from mouth and nose. (3) Active Decay: skin ruptures, releasing trapped gases; extensive maggot feeding, skin slippage, black putrefaction, and strong odor. (4) Advanced Decay: soft tissues largely consumed, insect activity decreases, vegetation around body dies from nitrogen purge. (5) Dry/Skeletonization: bones, cartilage, desquamated mummified tendons, and soil incorporation."
        ),
        (
            78,
            "How does a medical examiner differentiate between antemortem, perimortem, and postmortem bone fractures?",
            "Hard",
            ["bone fracture", "antemortem", "perimortem", "postmortem", "osteoblastic healing", "green bone response"],
            "Antemortem: bony callus/osteoblastic healing. Perimortem: green bone fracture (smooth spiral edges, hinging). Postmortem: brittle dry bone snap (right angle).",
            "Timing of skeletal trauma is established by osseous biomechanics: (1) Antemortem trauma occurs well before death and exhibits active physiological cellular repair: osteoclast resorption rounding fracture edges within 1-2 weeks, followed by woven bone formation, fibrocartilaginous soft callus, and hardened bony callus remodel. (2) Perimortem trauma occurs at or near the time of death while bone maintains living moisture and organic collagen elasticity (green bone fracture); characteristics include smooth, curved or spiral fracture lines, sharp edges, and plastic deformation (bone flakes and greenstick hinging). (3) Postmortem damage occurs to dry, brittle, mineral-depleted bone; fractures exhibit jagged, straight right-angle transverse breaks, lacking plastic deformation, with lighter surface patina on exposed broken faces."
        ),
        (
            79,
            "What is the difference between Cause of Death, Manner of Death, and Mechanism of Death?",
            "Easy",
            ["cause of death", "manner of death", "mechanism of death", "npathology", "autopsy", "coroner"],
            "Cause: disease/injury initiating fatal chain. Manner: legal circumstance (NASHU). Mechanism: specific biochemical/physiological disruption.",
            "In medicolegal death certification: (1) Cause of Death (COD) is the specific disease, injury, or toxic agent that initiates the lethal physiological sequence leading directly to death (e.g., 'Gunshot wound to the chest' or 'Atherosclerotic coronary artery disease'). (2) Manner of Death (MOD) is the legal circumstance explaining how the death arose, categorized into five classifications (NASHU): Natural, Accident, Suicide, Homicide, or Undetermined. (3) Mechanism of Death is the specific physiological or biochemical derangement produced by the cause of death incompatible with life (e.g., exsanguination, ventricular fibrillation, cardiac tamponade, cerebral herniation)."
        ),
        (
            80,
            "Explain the pathological findings in fatal hypothermia: paradoxical undressing and hide-and-die syndrome (terminal burrowing).",
            "Medium",
            ["hypothermia", "paradoxical undressing", "terminal burrowing", "wischnewski spots", "core temp"],
            "Discuss paralysis of hypothalamic vasomotor center causing sudden vasodilation (feeling hot), and primitive brainstem burrowing instinct.",
            "In fatal environmental hypothermia, as core body temperature drops below 30°C (86°F), two bizarre behavioral phenomena occur: (1) Paradoxical Undressing: severe hypothermia causes exhaustion of the brain's hypothalamic vasomotor center, leading to sudden loss of peripheral vasoconstriction; blood rushes back into cold cutaneous capillaries, creating a profound, deceptive sensation of intense heat that causes victims to strip off clothing shortly before death. (2) Terminal Burrowing (Hide-and-Die syndrome): an evolutionary brainstem defense mechanism where semi-conscious victims crawl under beds, into snowbanks, or behind furniture to create an insulated burrow. Autopsy reveals gastric mucosal Wischnewski erosions."
        ),
        (
            81,
            "What is the significance of the hyoid bone and thyroid cartilage fractures in suspected strangulation cases?",
            "Medium",
            ["hyoid bone", "thyroid cartilage", "manual strangulation", "ligature", "greater cornu", "ossification"],
            "Fracture of greater cornua indicates concentrated direct lateral neck compression (manual strangulation), correlated with age/ossification.",
            "The U-shaped hyoid bone sits in the anterior midline of the neck above the thyroid cartilage. In young individuals, the greater cornua are joined to the central body by flexible cartilaginous synchondroses that resist breaking. As age advances (>30-40 years), these joints ossify and become brittle. In manual strangulation (throttling), concentrated lateral fingertip compression drives the greater horns inward against the cervical spine, fracturing the hyoid bone (observed in ~20-35% of cases) or the superior horns of the thyroid cartilage. In hanging, suspension traction pulls the hyoid upward, rarely fracturing it compared to manual strangulation."
        ),
        (
            82,
            "How does a forensic pathologist differentiate true soot inhalation in respiratory airways from postmortem artifact in fire victims?",
            "Medium",
            ["soot inhalation", "fire death", "mucus", "carboxyhemoglobin", "bronchi", "cilia"],
            "True inhalation: soot trapped in sticky mucus deep in bifurcation of primary bronchi and microscopic alveoli, accompanied by mucosal edema.",
            "During a fire, passive settling of airborne soot into open mouth and external nostrils can occur postmortem. To confirm antemortem soot inhalation, the pathologist dissects the trachea, carina, and deep primary and secondary bronchi. Antemortem inhalation is demonstrated by fine carbon soot deeply adherent to sticky bronchial mucus, coating the tracheal mucosal bifurcations, and extending into tertiary bronchioles, accompanied by acute mucosal hyperemia and inflammatory thermal edema. Microscopic histology shows soot engulfed by alveolar macrophages, alongside elevated blood carboxyhemoglobin."
        ),
        (
            83,
            "What is 'tache noire' and how does it form on a corpse's eyes postmortem?",
            "Easy",
            ["tache noire", "postmortem change", "cornea", "sclera", "desiccation", "unclosed eyes"],
            "Reddish-brown/black horizontal ocular stripe caused by drying and desiccation of exposed sclera when eyelids remain unclosed.",
            "Tache noire (French for 'black spot') is a benign postmortem artifact occurring when the deceased's eyes remain unclosed or partially open after death. The horizontal strip of exposed sclera and cornea not protected by the eyelids is subjected to ambient air desiccation. Evaporation of moisture causes cellular drying and thinning of the conjunctival tissue, allowing underlying choroid melanin pigment to become visible as a dark reddish-brown to black band running horizontally across the eye. It is an indicator of postmortem exposure, not trauma or asphyxia."
        ),
        (
            84,
            "How does electrical injury cause death, and what are the microscopic hallmarks of an electrical entry mark?",
            "Hard",
            ["electrical mark", "electrocution", "ventricular fibrillation", "joule heating", "nuclear streaming", "micro-blister"],
            "Low-voltage (120V AC): ventricular fibrillation. Entry mark: Joule resistance heating causing intraepidermal micro-blisters and nuclear palisading.",
            "Death from alternating current (low-voltage 120-240V AC) is typically caused by electrical disruption of the cardiac conduction cycle, triggering fatal ventricular fibrillation. At the skin contact site, high tissue electrical resistance converts electrical energy into thermal energy according to Joule's Law (Q = I^2 R t). Macroscopically, electrical entry marks appear as circumscribed, crater-like, pale-gray lesions with elevated, puckered borders. Microscopically, the pathognomonic hallmark is 'nuclear palisading' or 'nuclear streaming'—elongated, stretched, hyperchromatic epidermal basal cell nuclei aligned parallel in the direction of current flow alongside subepidermal micro-blister cavities."
        ),
        (
            85,
            "What is the difference between a coroner system and a medical examiner system in death investigation?",
            "Easy",
            ["coroner", "medical examiner", "death investigation", "forensic pathologist", "board certified", "elected"],
            "Coroner: often elected layperson or official without medical training. Medical Examiner: appointed physician and board-certified forensic pathologist.",
            "The coroner system originated in medieval England; coroners are typically elected county officials who may be laypeople with no medical or scientific training (though they utilize contract pathologists for autopsies), responsible for administrative inquests into unexpected or violent deaths. The Medical Examiner (ME) system is a modern professionalized institution where the chief ME is an appointed licensed physician who has completed residency in anatomic pathology and an accredited fellowship in forensic pathology (board-certified by the American Board of Pathology), directly performing forensic autopsies and certifying death."
        ),

        # --- Trace Evidence, Materials & Crime Scene Dynamics (fs_86 to fs_100) ---
        (
            86,
            "Explain the '3R Rule' for determining the direction of impact force on fractured glass windows.",
            "Medium",
            ["glass fracture", "3r rule", "radial fracture", "concentric fracture", "conchoidal ridges", "direction of force"],
            "Radial fractures have Reverse/Right angles on the Rear (opposite side of the impact force).",
            "When a projectile or blunt object strikes a glass pane, it produces two types of fractures: (1) Radial fractures radiating outward from the point of impact like spokes, originating on the rear (tension) surface; and (2) Concentric circular fractures encircling the impact center, originating on the front (compression) surface. Along radial fracture edges, microscopic stress lines called Wallner lines or conchoidal ridges curve across the glass thickness. The 3R Rule dictates: 'Radial fractures form Right angles on the Reverse (rear) side of force'—meaning the perpendicular curve faces opposite to the surface that sustained the physical blow."
        ),
        (
            87,
            "How does Polarized Light Microscopy (PLM) identify synthetic and natural fibers in hit-and-run and assault cases?",
            "Hard",
            ["polarized light microscopy", "plm", "birefringence", "refractive index", "synthetic fibers", "pleochroism"],
            "Discuss crossed polarizers, isotropic vs anisotropic materials, sign of elongation, and Michel-Levy birefringence charts.",
            "Fibers are anisotropic materials possessing two distinct refractive indices along their parallel and perpendicular axes. Polarized Light Microscopy utilizes two polarizing filters aligned at 90° (crossed polars). When a fiber is rotated on the stage, it splits polarized light into orthogonal light rays traveling at different velocities, a property known as birefringence (delta n = n_parallel - n_perpendicular). By measuring the resulting retardation colors using a quartz compensator and referencing the Michel-Levy chart, examiners determine fiber cross-sectional thickness, sign of elongation, and polymer class (polyester, nylon, acrylic, cotton)."
        ),
        (
            88,
            "Explain the Becke Line method for determining the refractive index of microscopic glass fragments.",
            "Medium",
            ["becke line", "refractive index", "glass comparison", "immersion oil", "hot stage", "grim"],
            "A halo of light (Becke line) moves into the medium of higher refractive index as the microscope objective is raised; matches at vanishing point.",
            "The Becke line is a bright halo of focused light seen around the border of a transparent glass particle submerged in an immersion liquid under high magnification. When the microscope objective is racked upward (increasing focal distance), the Becke line always moves toward the medium with the higher refractive index (RI). In automated Glass Refractive Index Measurement (GRIM) systems, the immersion silicone oil is heated in a temperature-controlled hot stage. As oil temperature rises, its RI drops linearly until it matches the glass RI; at that exact temperature, the Becke line vanishes, determining glass RI to five decimal places."
        ),
        (
            89,
            "How are microscopic paint chips from automobile collisions analyzed across multiple layers using Pyrolysis GC-MS and FTIR?",
            "Hard",
            ["paint chip", "pyrolysis gc-ms", "ftir", "automotive paint", "clear coat", "primer surfacer"],
            "Analyze sequential layer cross-sections (primer, e-coat, basecoat, clearcoat); FTIR identifies organic binders; Py-GC-MS fragments polymers.",
            "Automotive paint systems consist of multiple micro-layers applied in a strict factory sequence: phosphate pre-treatment, electrocoat primer, primer-surfacer, color basecoat, and polyurethane clearcoat. A chipped paint flake contains a cross-sectional layer cake. Forensic analysts mount the chip in epoxy, polish the cross-section, and measure layer thicknesses, color sequences, and pigment inclusions under microscopy. Micro-FTIR spectroscopy identifies chemical functional groups in synthetic acrylic/melamine binder resins. Pyrolysis GC-MS thermally cracks non-volatile cross-linked polymers at 700°C into volatile fragments, producing a diagnostic pyrolysate fingerprint."
        ),
        (
            90,
            "Explain how the area of origin is calculated in Bloodstain Pattern Analysis (BPA) using impact angles and stringing/trigonometry.",
            "Hard",
            ["bloodstain pattern analysis", "bpa", "area of origin", "angle of impact", "arcsine", "tangent"],
            "Impact angle: sin theta = width / length. Area of convergence is 2D intersection; tangent of angle multiplied by distance yields 3D origin height.",
            "When blood droplets strike a surface obliquely, surface tension creates an elliptical stain. The acute angle of impact (theta) is calculated using trigonometry: sin(theta) = width of stain / length of stain (excluding the tail). Droplets in an impact spatter pattern originate from a common energetic source. By tracing the long central axis of multiple stains backward across the 2D surface, lines intersect at the two-dimensional 'Area of Convergence'. Measuring the distance (d) from each stain to the convergence point, the three-dimensional 'Area of Origin' height (h) is calculated: h = d * tan(theta), verified using physical stringing or laser trajectory software."
        ),
        (
            91,
            "Differentiate between cast-off, expirated, arterial spray, and transfer bloodstain patterns.",
            "Medium",
            ["bloodstain patterns", "cast-off", "expirated blood", "arterial spray", "transfer pattern", "vacuoles"],
            "Cast-off: linear swing arcs. Expirated: coughed blood with air bubble vacuoles. Arterial: high-pressure wave arches. Transfer: wet contact outline.",
            "Bloodstains reveal dynamic crime scene mechanisms: (1) Cast-off patterns: linear or curved trails of blood droplets flung from a swinging weapon (baseball bat, knife) as centrifugal acceleration overcomes blood surface tension during backswings. (2) Expirated blood: blood propelled from the nose, mouth, or airway by respiratory airflow or coughing, characterized by dilute coloration, irregular aerosol misting, and cellular air bubble vacuoles. (3) Arterial spray/gush: patterns produced by breaching high-pressure arterial vessels, exhibiting zig-zag waves, spines, and distinct pressure-drop peaks. (4) Transfer patterns: created when a wet, blood-bearing surface contacts another surface, leaving a recognizable imprint (e.g., bloody shoe sole or handprint)."
        ),
        (
            92,
            "How does Passive Headspace Concentration with Activated Charcoal Strips detect fire accelerants in arson investigations?",
            "Medium",
            ["arson", "accelerant extraction", "charcoal strip", "headspace gc-ms", "ignitable liquid residue", "elution"],
            "Sealed paint can with burned debris, heated at 60-80 C, charcoal strip adsorbs hydrocarbon vapors, eluted with carbon disulfide for GC-MS.",
            "Charred fire debris is sealed immediately in airtight, clean metal paint cans to trap volatile Ignitable Liquid Residues (ILRs) like gasoline, kerosene, or diesel. In Passive Headspace Concentration (ASTM E1412), an activated charcoal strip (carbon polymer wafer) is suspended inside the sealed can, which is baked in an oven at 60–80°C for 2 to 16 hours. Vaporized petroleum hydrocarbons adsorb onto the massive internal surface area of the activated charcoal. The strip is removed, and hydrocarbons are desorbed with a minute volume (50-100 uL) of carbon disulfide (CS2) or dichloromethane, then injected into GC-MS for hydrocarbon profile pattern matching."
        ),
        (
            93,
            "What chromatographic patterns distinguish weathered gasoline from weathered diesel fuel in arson GC-MS spectra?",
            "Hard",
            ["gasoline", "diesel", "weathered accelerant", "arson", "n-alkanes", "btex"],
            "Gasoline: BTEX aromatics and alkylbenzenes in early retention times. Diesel: broad homologous series of n-alkanes (C10 to C24) forming a Gaussian envelope.",
            "Evaporation and thermal weathering degrade volatile accelerants, causing lighter components to burn away first. Gasoline is an aromatic-rich light petroleum distillate; its GC-MS spectrum is dominated by aromatic hydrocarbons: benzene, toluene, ethylbenzene, and xylenes (BTEX), plus alkylbenzenes (propylbenzenes, trimethylbenzenes) and indanes. Diesel is a medium-to-heavy petroleum distillate; its chromatogram displays a prominent, regular homologous series of straight-chain normal alkanes (n-alkanes from C9 to C25) spaced at constant retention intervals forming a characteristic unimodal Gaussian boiling-point distribution curve."
        ),
        (
            94,
            "How do forensic examiners differentiate human hairs from non-human animal hairs under microscopic examination?",
            "Easy",
            ["hair examination", "medullary index", "cuticle scales", "cortex", "pigment granules", "species identification"],
            "Medullary index: <0.33 for humans, >0.5 for animals. Animal cuticle scales can be spinous/coronal; humans are imbricate. Medulla structure differs.",
            "Hair analysis relies on three morphological layers: cuticle (outer scales), cortex (pigment layer), and medulla (central core). (1) Medullary Index: the ratio of the medulla diameter to overall hair shaft diameter; in humans, the medullary index is narrow, less than 0.33 (one-third), whereas in animals it is wide, greater than 0.50 (one-half). (2) Cuticular Scales: human hair exhibits exclusively flattened, overlapping imbricate scales; animals exhibit diverse coronal (crown-like) or spinous (petal-like) patterns. (3) Pigment Granules: in humans, melanin granules are distributed uniformly toward the outer cortex; in animals, pigment is concentrated centrally around the medulla."
        ),
        (
            95,
            "Explain how Electrostatic Detection Apparatus (ESDA) recovers indented writing impressions on questioned documents.",
            "Medium",
            ["esda", "questioned documents", "indented writing", "electrostatic detection", "corona discharge", "toner"],
            "Polyester film over paper, charged with corona wand, paper indented areas retain electrostatic charge, dark toner cascade reveals indented strokes.",
            "When handwriting is executed on a top sheet of paper, pen tip pressure creates invisible microscopic plastic indentations in underlying blank pages of the notepad. The Questioned Document is placed on a porous brass vacuum platen of the ESDA, covered with a thin Mylar (polyester) imaging film, and held down by vacuum. A high-voltage corona wire moves across the surface, depositing an electrostatic charge across the film. Microscopic indentations cause localized electrostatic charge variances. When black toner powder is cascaded across the tilted platen, negatively charged toner particles cling to the indented paths, revealing sharp, legible writing impressions up to 5-7 pages deep."
        ),
        (
            96,
            "How does Thin Layer Chromatography (TLC) and Video Spectral Comparators (VSC) analyze questioned inks and altered documents?",
            "Medium",
            ["vsc", "video spectral comparator", "thin layer chromatography", "ink analysis", "infrared luminescence", "metamerism"],
            "VSC: non-destructive multi-wavelength UV-vis-IR lighting exposing ink metamerism. TLC: micro-punch plug separates chemical ink dye dyes.",
            "Document examiners use non-destructive optical testing before chemical destruction. A Video Spectral Comparator (VSC) illuminates questioned documents with selective narrow-band wavelengths from ultraviolet to infrared while viewing through barrier filters. Inks that look identical in daylight (metamerism) behave differently under Infrared Luminescence: one ink may fluoresce bright green under 800 nm while a fraudulent addition remains dull black. For chemical confirmation, a tiny micro-punch (0.5 mm) of the ink line is extracted in pyridine/methanol and spotted on a silica gel Thin Layer Chromatography (TLC) plate to separate diagnostic dye components."
        ),
        (
            97,
            "What is a hardware write-blocker, and why is cryptographic hashing (MD5, SHA-256) mandatory in digital forensics?",
            "Easy",
            ["digital forensics", "write-blocker", "md5", "sha-256", "cryptographic hash", "chain of custody"],
            "Write-blocker intercepts OS write commands to preserve original drive bit-stream. Cryptographic hash verifies forensic duplicate is 100% identical bit-for-bit.",
            "In digital forensics, any alteration of digital storage media invalidates evidence in court. A hardware write-blocker is a physical bridge connected between the suspect storage drive and the forensic workstation; it physically or micro-programmatically blocks incoming SCSI/SATA/USB write commands from the host OS while permitting read-only access. Forensic examiners create a bit-stream disk image (E01 or raw DD format). Before and immediately after imaging, a mathematical cryptographic hash function (SHA-256 and MD5) computes a fixed alphanumeric digest of the entire drive. Matching hash values proves that the forensic duplicate is bit-for-bit identical to the original seized media."
        ),
        (
            98,
            "Explain the difference between volatile RAM acquisition and non-volatile dead-box forensics.",
            "Medium",
            ["volatile ram", "memory analysis", "dead-box forensics", "order of volatility", "encryption keys", "volatility framework"],
            "Volatile RAM is lost at power-off, contains running processes, cleartext passwords, decrypted keys. Dead-box images powered-down disk drives.",
            "RFC 3227 establishes the Order of Volatility for digital evidence: volatile data that is lost upon system shutdown must be collected first. Live RAM acquisition connects a trusted USB tool to dump volatile system memory from a running computer before pulling the power plug. RAM contains ephemeral artifacts: decrypted BitLocker encryption keys, active network socket connections, injected in-memory malware, cleartext passwords, and unencrypted chat logs. Non-volatile 'dead-box' forensics is conducted on powered-down physical hard disk drives and SSDs, analyzing persistent file systems, Master File Tables (MFT), registry hives, and event logs."
        ),
        (
            99,
            "What is file carving in digital forensics, and how does it recover deleted files without file system metadata?",
            "Medium",
            ["file carving", "data carving", "magic numbers", "file headers", "file footers", "unallocated space"],
            "Carving scans unallocated raw sectors for file signatures/magic numbers (e.g., JPEG starts FF D8 FF, ends FF D9) to extract file contents.",
            "When a user deletes a file, the operating system merely marks the file system table pointers (e.g., NTFS Master File Table record or FAT directory entry) as free and deallocated, while the actual raw data blocks remain intact on disk sectors until overwritten. File carving is a recovery technique that bypasses the file system entirely, scanning raw unallocated disk sectors for standardized file signatures or 'magic numbers' in binary hex. For instance, a JPEG image begins with file header hex bytes 'FF D8 FF' and terminates with footer 'FF D9'. The carving tool isolates the block between header and footer, reconstructing the original file."
        ),
        (
            100,
            "What is the Chain of Custody, and what legal consequences arise if a critical gap is discovered during trial?",
            "Easy",
            ["chain of custody", "evidence handling", "admissibility", "tampering", "transfer log", "evidence integrity"],
            "Meticulous, unbroken paper trail tracking every individual who possessed the evidence; gaps allow defense to argue tampering, leading to exclusion.",
            "The Chain of Custody is a comprehensive, chronologically unbroken paper trail and electronic log that documents the seizure, custody, transfer, analysis, storage, and disposition of physical and digital evidence. Every entry logs the date, exact time, releasing individual, receiving individual, purpose of transfer, and evidence tamper-evident seal serial numbers. If an unexplained gap or unauthorized possession is uncovered, the trial court may sustain defense objections that the evidence was contaminated, substituted, or tampered with, resulting in total exclusion of the physical evidence and suppression of all downstream laboratory results under the exclusionary rule."
        )
    ]

    questions = []
    for item in questions_raw:
        q_id, text, diff, kw, tips, ans = item
        questions.append({
            "id": f"fs_{q_id}",
            "text": text,
            "difficulty": diff,
            "keywords": kw,
            "tips": tips,
            "model_answer": ans
        })
    return questions


if __name__ == "__main__":
    qs = get_fs_questions()
    print(f"Generated {len(qs)} Forensic Science questions (IDs: {qs[0]['id']} to {qs[-1]['id']})")
