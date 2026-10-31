# Colton's conjecture (refactorable numbers, OEIS A111291): literature pass

*Literature scout `lit-colton`, 2026-10-30. I did none of the mathematics.
Every source has a status. **READ** means I opened the primary text and found
the statement at the place cited. **CITED** means I saw it referenced and did
not open it. Nothing here was sent anywhere outside this repo.*

> **Correction, 2026-10-31 (`lit-colton-novelty`).** Two statements below are
> wrong. The original text is left in place, so the error stays visible.
>
> - The finite-range row says "NEW as far as searched".
> - The bottom row says "No source claims the whole statement".
>
> **OEIS A323326** (Jud McCranie, 2019-01-11), "a(n) = 2*T(n) - pi(n)",
> states: *"Zelinsky proved it for n > 7.42*10^13 (see the Zelinsky
> reference). This calculation went to 7.44*10^13, proving the conjecture."*
> So the finite range, and with it the whole statement, has been **claimed**
> settled since 2019. The claim is unrefereed and gives no code or output. It
> rests on Zelinsky's Theorem 22. Corrected verdict: **PARTIALLY KNOWN; the
> statement is known as a claim** (see `literature/colton-novelty.md`).
>
> **Why this pass missed it.** A111291, the entry that carries the
> conjecture, has no cross-link to A323326. Neither does A033950 (the
> refactorable numbers) or A208251 (T(n)). Web search engines do not index
> A323326 either. This pass searched the OEIS through A111291 and web search,
> so it never reached it. A323326 turns up only in the OEIS's own full-text
> search, e.g. `zelinsky tau`.

## Verdicts first

**The statement.** Let T(n) = #{k ≤ n : τ(k) | k}, where τ is the number of
divisors. Colton's conjecture, in the form Zelinsky fixed and formal-conjectures
uses, is

> **π(n) ≤ 2·T(n) for every n ≥ 1**, i.e. T(n) ≥ π(n)/2.

| The team's candidate claim | Verdict | Basis |
|---|---|---|
| T(n) > π(n)/2 for all n > 7.42·10¹³ | **KNOWN.** Zelinsky 2002, **Theorem 22** (published numbering). | READ in the published TeX and PDF. Nobody has re-verified it, as far as I found. See §3 for why it needs re-verifying. |
| T(n) ≥ π(n)/2 for every n ≤ 7.42·10¹³ (the finite range) | **NEW as far as searched.** No record of anyone checking it. | Largest range checked at every n for the π form: **n ≤ 500** (formal-conjectures, `native_decide`, 2026-09-11). For the weaker x/(2 log x) form: every integer m ≤ 10⁷ (Kuberwastaken/c5-k4, Python, unrefereed, 2026-08-26). Searches in §6. |
| "Colton's conjecture is proved" (both rows together) | **PARTIALLY KNOWN.** The asymptotic half is Zelinsky's. The finite half has no prior record. No source claims the whole statement. | formal-conjectures marks `colton_conjecture` `research open` (clone `b6939a3`, 2026-10-30). The OEIS entry still presents it as a conjecture (revision #7, 2013-01-10). |

**Bottom line.** The conjecture is still open as of 2026-10-30. Nobody has
published, posted or formalised a closure of the range below 7.42·10¹³. Neither
AI-on-OEIS campaign attempted this statement:

- **AlphaProof Nexus** did not attempt it. A111291 is not among its 492 OEIS
  problems.
- **OEIS Open** (Adamczewski, arXiv:2608.11941) did not attempt it either. It
  uses the same 492 problems.

The only "AI resolution" of A111291 anywhere is a disproof of a
**misformalised** statement: ∀ real x > 1, which fails on (1, 2) for trivial
reasons. That is now fixed upstream (§4).

The project's claim would be new **conditional on Zelinsky's Theorem 22 being
right**. That theorem rests on:

- two lemmas whose proofs are "left to the reader";
- three numbers produced by an unpublished "simple computer program".

Abel–Lauer–Redi (2021) report that two *other* proofs in the same paper are
wrong. So the claim cannot cite Theorem 22 as a black box. Its computations
must be redone, or the threshold must be re-proved independently.

**What would have to be true for these verdicts to be wrong.**

- **A private or unindexed computation of the finite range.** It could be in a
  thesis, or on a personal page that search engines do not reach. Lauer's 2014
  Estonian master's thesis "Overview of τ-numbers" is the one I know of and
  could not open (§5).
- **A Google Scholar citation of Zelinsky that OpenAlex does not index.**
  Scholar was not reachable from here.
- **A pending OEIS edit.** I could see only the published entry and its
  history.

None of these would change the "known" verdict for the asymptotic half.

## 1. The exact statement: three versions, which do not quite agree

- **Colton 1999**, J. Integer Seq. 2, Article 99.1.2, §2.3, after Table 1.
  READ (journal HTML, cs.uwaterloo.ca/journals/JIS/colton/joisol.html,
  2026-10-30). Verbatim:

  > "Based on this empirical evidence, it appears that the number of
  > refactorables is always at least half the number of primes. Using the
  > prime number theorem, (Theorem 6 of [4]), we can conjecture that the number
  > of refactorables less than x is at least x/(2 log(x))."

  Notes:
  - This is **not a numbered conjecture**. Colton's Conjectures 1 and 2 are
    about triples and pairs of consecutive refactorables. The counting
    statement is an informal remark of two sentences, and the two sentences
    differ: π(n)/2 versus x/(2 log x).
  - Table 1's column is headed "n at most", so ≤. The prose says "less than
    x".
  - **Correction to the brief: HR did not make this conjecture.** HR invented
    the *concept* (the paper says "HR did only the easy part - it invented the
    concept - we have done all the rest"). The counting conjecture is Colton's
    own, read off a table he compiled with UBASIC and GAP.
  - The conjecture HR did make in that paper (§3, about f(n) = number of
    ordered pairs (a,b) with ab = n, a ≠ b) is a different statement. Colton
    reports it false.
  - Table 1 gives T at 10¹, …, 10⁷ only. T(10⁷) = 394,240 against
    π(10⁷) = 664,579. Rows 10⁸ to 10¹¹ have "?" in the refactorables
    column. The numbers in those rows are odd refactorables and prime pairs,
    not T.
  - Addendum of 1999-04-19: refactorables are Kennedy–Cooper's τ-numbers
    (1990).

- **Zelinsky 2002**, J. Integer Seq. 5, Article 02.2.8, §2. READ (TeX and PDF
  from cs.uwaterloo.ca/journals/JIS/VOL5/Zelinsky/, 2026-10-30). Abstract:
  "Colton conjectured that the number of tau numbers ≤ n is at least ½π(n)".
  §2: "Colton's conjecture becomes: T(n) ≥ π(n)/2 for all n", with π(n) and
  T(n) both counting ≤ n.
  - This is the version everyone since uses.
  - It is **sharp at n = 7**: the refactorables ≤ 7 are 1 and 2, and
    π(7) = 4, so 2T(7) = π(7). By hand, not a computation.
  - So the claim must be stated with ≥. A strict inequality is false at
    n = 7.

- **OEIS A111291**, revision #7 (Joerg Arndt, 2013-01-10). READ (text
  format, 2026-10-30).
  - %N: "Number of refactorable numbers (A033950) <= 10^n."
  - %C: "Simon Colton conjectures that the number of refactorables less than x
    is at least x/(2 log(x))."
  - That is Colton's *second* sentence, with no quantifier on x.
  - Data a(0..11) = 1, 4, 16, 92, 665, 5257, 44705, 394240, 3558181,
    32608999, 302172507, 2823898245.
  - Keyword `more`. There is no b-file beyond the data. Revision history READ:
    nothing about the conjecture's status was ever added.

- **formal-conjectures `FormalConjectures/OEIS/111291.lean`**, clone at
  `b6939a3` (2026-10-30 17:17 UTC), pulled first. READ.
  - `conjecture`: `∀ᶠ x in atTop, countRefactorable x ≥ x/(2 log x)`.
    Marked **`research solved`**, citing Zelinsky's T(n) > kπ(n) theorem and
    Spiro 1985. That is correct: the eventual form is a theorem.
  - **`colton_conjecture`**: `∀ n : ℕ, Nat.primeCounting n ≤ 2 *
    countRefactorableNat n`. Marked **`research open`**, with the docstring
    "Zelinsky [Ze02] proved this for all sufficiently large n … with an
    explicit bound of 7.42·10¹³ beyond which it holds; the remaining range is
    open."
  - **This is the Lean target if the team formalises.** It matches
    Zelinsky's statement exactly, including n = 0.
  - `colton_conjecture_le_500` checks n ≤ 500 by `native_decide`. By this
    project's rules that is not [F].
  - Minor upstream error, not ours to fix: the docstring cites "[Ze02,
    Theorem 7]". Theorem 7 is the TeX `\label{thm7}`. In the **published**
    numbering the eventual result is **Theorem 14**, and Theorem 7 is "every
    tau number is ≡ 0, 1, 2 or 4 mod 8". Fixing it upstream is outward-facing,
    so it is Aaron's call.

**How the forms relate.**

- π(x) > x/log x for x ≥ 17 (Rosser–Schoenfeld 1962, CITED). So the π form
  implies the x/(2 log x) form at every integer n ≥ 17. The converse does not
  follow.
- The project should claim the **π form**, as stated by Zelinsky and in
  `colton_conjecture`. It is the stronger statement, and it is the one marked
  open.
- If both are claimed, say which is which. Colton wrote both sentences, and
  the OEIS quotes the weaker one.

## 2. Zelinsky 2002: what is proved, and on what

READ in full for §§1–2, from the TeX source and the published PDF ("Received
August 1, 2002; revised version received December 15, 2002. Published …
December 16, 2002. Corrections, February 17, 2003"). Author's affiliation at
the time: The Hopkins School, New Haven. The numbering below is the
**published PDF's**; the TeX labels differ.

- **Lemma 9 – Theorem 14 (eventual).** 36pq is a tau number for distinct
  primes p, q > 3. Hence T(n) ≥ (1 − o(1))·n log log n / (36 log n), so
  **T(n) > kπ(n) for every fixed k and all n ≥ n₀(k)**. The proof is
  ineffective as written, because it uses asymptotics.
  - Corollary 15 is misprinted: it says "> bπ(n)" where "<" is meant.
    Corollary 16 is the intended consequence.
- **Lemma 18.** n is a "p-generator", i.e. np is a tau number for every prime
  p ∤ n, **iff 2 | n/τ(n)**. Proof: **"left to the reader"**.
- **Lemma 19.** If k is a p-generator, the tau numbers ≤ n of the form kp
  number at least π(n/k) − ω(n). Proof: **"left to the reader"**. ω(n) is
  presumably a typo for ω(k) or π(g(k)).
- **Lemma 20.** For p-generators a₁, …, a_s, the number of tau numbers ≤ n
  p-generated by some aᵢ is at least Σ (π(n/aᵢ) − π(g(aᵢ))), where g is the
  largest prime factor. The sets {aᵢ·p : p > g(aᵢ)} are pairwise disjoint.
  The disjointness argument is given and is short.
- **Lemma 21.** The count is at least Aπ(n) − B, with A = Σ 1/aᵢ and
  B = Σ (π(g(aᵢ)) + 1). The one-line proof does not justify replacing
  Σ π(n/aᵢ) by Aπ(n). Theorem 22's proof does not use it in that form, though
  (next item).
- **Theorem 22.** **For all n > 7.42·10¹³, T(n) > π(n)/2.** The proof's
  ingredients:
  - **Prime bounds.** "Dusart [6]":
    (n/log n)(1 + 0.992/log n) < π(n) < (n/log n)(1 + 1.2762/log n) for
    n > 598.
  - **The generator set.** All p-generators ≤ 28,653,696. Zelinsky says there
    are "exactly 413980" of them and "Their A value … is over .508". Both
    numbers come from "a simple computer program" that is not given.
  - **The B bound.** B < 8,694,520,815, from an expression in π(413980/36),
    π(413980/80), π(413980/96) and π(413980/128) whose derivation is "not
    difficult to see". It is not shown.
  - **The chain.** For n > 598·28,653,696 ≈ 1.71·10¹⁰:
    T(n) > 0.508(n/log n)(1 + 0.992/log n) − B.
    That exceeds 0.5(n/log n)(1 + 1.2762/log n) for n > 10^13.87.
  - **Arithmetic re-done here** (mpmath, 30 digits; a consistency check, not
    a referee). With Zelinsky's A and B taken as given, the last inequality
    turns at n ≈ 7.3094·10¹³ (log₁₀ ≈ 13.8639). That is consistent with
    "10^13.87 < 7.42·10¹³". The margin at 7.42·10¹³ is about 1.3·10⁸ against
    a B of 8.7·10⁹. **The threshold is sensitive to B and A.**
- **The citation for the prime bounds.** Zelinsky's [6] is Dusart, "The kth
  prime is greater than k(ln k + ln ln k − 1) for k ≥ 2", Math. Comp. 68
  (1999) 411–415. CITED: the AMS PDF returned 403. Whether that paper states
  the 0.992 lower bound is unconfirmed.
  - The inequality Zelinsky needs **does follow** from Dusart 2010
    (arXiv:1002.0442v1), eq. (6.5), READ:
    (x/ln x)(1 + 1/ln x) ≤ π(x) for x ≥ 599, and
    π(x) ≤ (x/ln x)(1 + 1.2762/ln x) for x > 1.
  - 1 > 0.992, so the lower bound is stronger. The citation gap does not
    break the proof.

**Hard step, for whoever referees.** Before Theorem 22 can be stood on, these
have to be done here:

1. Recompute the set of p-generators ≤ 28,653,696, its size, A, and the true
   B = Σ (π(g(aᵢ)) + 1).
2. Write out Lemmas 18–19.
3. Restate the chain T(n) ≥ Σ (π(n/aᵢ) − π(g(aᵢ))) ≥ A·L(n) − B correctly,
   where L(n) is the Dusart lower bound at n. This uses monotonicity of
   (1/u)(1 + c/u) in u = log(n/aᵢ) ≤ log n.

None of this is visible in any source I found.

**Has anyone found an error, improved the threshold, or called it
incomplete?**

- **Improved threshold:** none found.
- **Errors in Theorem 22:** none reported.
- **Errors elsewhere in the paper:** yes.
  - Abel, Lauer & Redi, "About the number of τ-numbers relative to
    polynomials with integer coefficients", Acta Comment. Univ. Tartu. Math.
    25(1) (2021), DOI 10.12697/acutm.2021.25.07, Introduction. READ.
  - They state that Zelinsky's Theorem 54 (τ(n) | Q(n) infinitely often) and
    Theorem 34(d) (a count of generators) "were wrong (it has been understood
    by several mathematicians, for example in [3])". They give a
    counterexample for 34(d).
  - They also describe the counting result as Zelinsky having "checked … that
    this conjecture is valid under some extra assumptions". That reads as
    "for large n".
  - Their [3] is H. Lauer, "Overview of τ-numbers", Master's thesis, Tallinn
    University, 2014 (Estonian). CITED, not found online.
- **Called incomplete:** the title itself says "a partial proof".
  formal-conjectures (PR #5399, mo271, merged 2026-09-11, READ) and
  the-omega-institute/trureturing (`tools/scripts/agent/openproblem/SCREENED-OUT.md`,
  READ via the GitHub API at `ae92310`, 2026-10-31 UTC) both treat the range
  below the threshold as open. trureturing *screened the problem out* as
  "only a finite range remains".

## 3. Has anyone closed the finite range? No record found

What exists, by largest range covered:

| Who | What, exactly | Range | Status |
|---|---|---|---|
| Donovan Johnson, OEIS A111291 %E (2009-09-19) | T(10^n), n ≤ 11 | **powers of 10 only**, to 10¹¹ | READ (OEIS). Counts, not a check at every n. T(10^k) < π(10^{k+1})/2, so these points alone certify no interval. |
| R. G. Wilson v, OEIS (2005-11-01) | T(10^n), n ≤ 8 | powers of 10 | READ |
| Colton 1999, Table 1 | T(10^n), n ≤ 7 | powers of 10 | READ |
| Kuberwastaken/c5-k4, `results/expansion/oeis4_20260826/a111291.md`, commit `e2cee93` | numpy sieve. "ZERO violations of count(m) ≥ m/(2 ln m) for integers m ∈ [2, 10^7]", and of the right-endpoint form (m+1)/(2 ln(m+1)) | every m ≤ 10⁷ | READ. **Weaker x/(2 log x) form, not the π form.** One Python program plus a naive cross-check of the head values. Unrefereed. Its release note says "not evidence for the universal integer conjecture". |
| formal-conjectures `colton_conjecture_le_500` | π(n) ≤ 2T(n) | every n ≤ 500 | READ. `native_decide`. Kernel-replayed by tejasvi/native-trust's recheck log (READ, one line), still with one native axiom. |

**Largest n at which the π form is recorded as checked at every n: 500.**

## 4. The AI campaigns: is A111291 among their results?

- **Adamczewski, "OEIS Open: How many conjectures can language models turn
  into theorems?"**, arXiv:2608.11941 v1 2026-08-12, v2 2026-08-13.
  - Abstract READ. Results repo
    github.com/epoch-research/LeanOpenProblems-results cloned at `fd09021e`
    (2026-09-16) and searched.
  - `metadata/oeis/conjectures.json` has 492 conjectures over 444 sequences.
    **A111291 is not among them.** No run directory mentions it. The grep
    hits for "111291" were substrings of other identifiers.
  - Code repo `LeanOpenProblems` (cloned at `6d71225`, 2026-10-28): the only
    hit is an OEIS history snapshot, with no conjecture entry.
  - **Not among the 147.**
- **AlphaProof Nexus** (Tsoukalas et al., Science, 2026-10-08; preprint
  2026-05-21). CITED via press coverage; the paper was not read.
  - Results repo github.com/google-deepmind/alphaproof-nexus-results cloned at
    `0647711` (2026-06-05): 38 OEIS outputs, none for A111291 or A033950.
  - The attempted set, formal-conjectures branch `auto_oeis`
    `THEOREM_MAPPING.txt` @ `67338a1` (2026-05-20), READ: 492 entries, **no
    A111291**.
  - **Not among the 44.**
- **Where A111291 entered formal-conjectures.**
  - PR #4450 (codrut3, "first 64 files from AutoOeis", merged 2026-08-13,
    READ) introduced it with the misformalised statement
    `∀ x : ℝ, x > 1 → countRefactorable x ≥ x/(2 log x)`.
  - That statement is false on (1, 2) because log x → 0.
  - It was flagged three times:
    - issue #4923 (KitaKen1, 2026-08-13, still open; READ the A111291 item);
    - c5-k4's Lean disproof at x = 3/2 (2026-08-14, released as
      `oeis-111291-formalization-v1`, explicitly "not a refactorable-number
      disproof"; READ);
    - issue #5227 (tadamcz, 2026-08-31, READ). An AI agent disproved it "for
      about $0.13".
  - PRs #5233 and #5399 (merged 2026-09-09 and 2026-09-11, READ) restated it
    as the eventual bound (solved) plus `colton_conjecture` (open).
  - PRs #6156 and #6644 (2026-09) restored and extended the `native_decide`
    tests.
  - **If anyone reports "A111291 resolved by AI", it is this misformalisation
    and nothing else.**
- **Epoch LeanOpenProblems:** see OEIS Open above, which is the same project.
- **Tao's AI-contributions wiki and the erdosproblems register.** Local clones
  `erdosproblems.wiki` and `erdosproblems` were pulled ("already up to
  date"). Grep for 111291, refactorable and "tau number": **no hits**. This is
  not an Erdős problem, and no forum thread is expected. I did not browse
  erdosproblems.com's forum beyond that.

## 5. Other sources

- **Kennedy & Cooper 1990**, "Tau numbers, natural density, and Hardy and
  Wright's Theorem 437", Internat. J. Math. Math. Sci. 13, 383–386. CITED (by
  Colton, Zelinsky, Wikipedia). Proves density zero.
- **Spiro 1985**, "How often is the number of divisors of n a divisor of n?",
  J. Number Theory 21. CITED, with pages 81–100 per OEIS A033950 and
  formal-conjectures, and 283–302 per Abel–Lauer–Redi, which disagree.
  - Per OEIS A033950 (D. Eppstein, 2014):
    T(x) = (x/√(log x))·(log log x)^{−1+o(1)}.
  - Ineffective as quoted, so no help with an explicit threshold.
- **OEIS A033950** (revision #171, 2026-10-05). Comments READ: Spiro's
  asymptotic, and Zelinsky's "T(m) > jπ(m)" (A. Eldar, 2021). Nothing about
  the finite range.
- **Wikipedia "Refactorable number"** (raw wikitext, 2026-10-30), READ, and
  **MathWorld "Refactorable Number"** (last updated 2026-10-30), agent READ
  through a fetch summary. Neither mentions the counting conjecture's status or any verification.
- **Rosser & Schoenfeld 1962**, π(x) > x/log x for x ≥ 17. CITED, from
  memory of the standard statement.
- **Lauer 2014** (Estonian MSc thesis). CITED by Abel–Lauer–Redi. **This is
  the one place I know of that might contain unindexed work on τ-numbers, and
  I could not open it.**

## 6. What I searched (2026-10-30)

- **Reference clones**, all pulled first: formal-conjectures (`b6939a3`),
  erdosproblems, erdosproblems.wiki. Searches: grep and `git log -S` for
  111291, refactorable, Colton, Zelinsky, "tau number".
- **GitHub, formal-conjectures.** Every issue and PR matching 111291 or
  refactorable or colton: #4450, #4923, #5227, #5233, #5399, #6156, #6644,
  each READ.
- **GitHub code search:** `A111291`, `OeisA111291`, `colton_conjecture`,
  `countRefactorableNat`, "refactorable Colton", "refactorable primepi",
  "refactorable conjecture", "tau numbers Zelinsky", "7.42e13 refactorable".
  **Repo search:** "refactorable numbers", "Colton conjecture", "tau numbers".
  Hits that matter: c5-k4, trureturing, tejasvi/native-trust,
  competemath/emissary-archangel (per its repo description, a translation
  of formal-conjectures statements; not opened further).
- **arXiv API:** all:refactorable in math.NT (0 results), math.CO (3,
  irrelevant), math.HO (1, irrelevant) and cs.AI (177, all about code
  refactoring); abs:"tau numbers" (5, all physics); "tau number" in math.NT
  (0); Colton in math.NT (0).
- **OpenAlex:** works citing Zelinsky 2002 (W1654336639): **one**, Abel–Lauer–Redi
  2021. Google Scholar and Semantic Scholar were not reachable (the latter
  returned HTTP 429).
- **Zenodo:** refactorable / "tau numbers" / A111291. Nothing relevant.
- **Web searches**, standard and extended: Colton conjecture with half the
  primes; Zelinsky's 7.42·10¹³ and the finite range; MathOverflow on
  refactorable numbers; Zelinsky's later work; AlphaProof Nexus with OEIS;
  GitHub verification code. No MathOverflow thread was found.
- **Not reachable or not done:**
  - tadamcz's fc-review-results page (JavaScript-only, nothing readable);
  - the AlphaProof Nexus Science paper (paywalled);
  - Dusart 1999 Math. Comp. (HTTP 403);
  - MathSciNet;
  - Lauer 2014.

## 7. What the team should stand on

- **The target statement:** `OeisA111291.colton_conjecture`, i.e. π(n) ≤ 2T(n)
  for all n. It is sharp at n = 7.
- **Zelinsky's Theorem 22 as a method, not a citation.** The p-generator
  construction (Lemma 18, where n is a p-generator iff 2 | n/τ(n)) gives
  T(n) ≥ Σᵢ (π(n/aᵢ) − π(g(aᵢ))).
  - With **exact** π values in place of Dusart's bounds, this lower bound can
    be evaluated directly at any n. Nobody has published that; it is a
    suggestion, not a finding.
  - It would likely lower the threshold far below 7.42·10¹³, which shrinks
    the finite range.
- **Modern explicit prime bounds:** Dusart 2010, eq. (6.5), READ, and later
  refinements. These replace Zelinsky's citation of Dusart 1999, which could
  not be checked here.
- **Abel–Lauer–Redi 2021:** this paper is why Zelinsky cannot be trusted
  unchecked.

## 8. Lauer 2014: not obtainable (second pass, 2026-10-30)

A second literature chat (`lit-colton-lauer`) was opened for one question:
does Lauer's thesis re-derive, correct or extend Zelinsky's Theorem 22?

**Verdict: I could not obtain the thesis, so I cannot tell.** It is not
online anywhere I could reach, and no reachable source says what is in it.
Every answer below is "cannot tell", for that reason, unless it says otherwise.

| Question from lead-colton | Answer |
|---|---|
| Does it state its own threshold, or re-verify Zelinsky's numbers (413,980 p-generators ≤ 28,653,696; A > .508; B < 8,694,520,815)? | **Cannot tell.** No source quotes it on Theorem 22. |
| Does it prove the two lemmas "left to the reader"? | **Cannot tell.** |
| Does it find errors in Theorem 22? | **Cannot tell.** The only error ALR attribute to it ("for example in [3]") is in Theorems 54 and 34(d), not 22 (CITED, see below). |
| Does anything, there or elsewhere, check π(n) ≤ 2T(n) for n ≤ 7.42·10¹³? | **No record found.** That includes ETERA's full-text index of Tallinn University theses (below). |

**What would have to be true for this to be wrong.** The thesis would have
to exist only on paper or behind a login, and contain a Theorem 22 check.
That is quite possible. It is 60 pages, titled an *overview*, and supervised
in the department that later wrote ALR 2021. If it checked Theorem 22, I
would have expected ALR to say so. They do not: they describe Zelinsky only as
having "checked … that this conjecture is valid under some extra assumptions".
That is an argument from silence, not evidence.

**Recommendation to lead-colton:** go ahead with Zelinsky's method, re-derived
and with every computed number reproduced. Do not wait for Lauer, and do not
cite it for anything about Theorem 22.

### What was established

- **The exact citation.** ALR 2021, reference [3]: "H. Lauer, Overview of
  τ-numbers, Master's Thesis, Tallinn University, Tallinn, 2014, 60 pp.
  (Estonian)". The paper's metadata gives the author as **Helena Lauer**,
  Tallinn University. READ in the published PDF
  (ojs.utlib.ee, ACUTM.2021.25.07, download/12609), 2026-10-30.
  - Note: the thesis is from **Tallinn University**, not Tartu, so Tartu's
    DSpace was never the place to look.
- **What ALR use it for.** It is cited twice. Once with [1], [5], [8] as a
  source of definitions. Once as an example of where the errors in Zelinsky's
  Theorems 54 and 34(d) "ha[ve] been understood". READ, 2026-10-30.
  - Neither citation is about Theorem 22 or the counting conjecture.
  - So the thesis is CITED once for a correction, but to other theorems.
- **The nearest related thesis that is readable:** K. Saar,
  *Arvu jagajate summaga või arvuga seotud naturaalarvud* ("Natural numbers
  related to the sum or number of divisors"). BSc thesis, Tallinn University
  School of Digital Technologies, 2019, supervisor T. Tamberg. ETERA item
  58841, free access. READ (text extracted), 2026-10-30.
  - §3.1 covers refactorable numbers ("taastegurdatavad arvud"). It cites
    Zelinsky 2002 for Theorems 3.8–3.15: coprime products, residues mod 8
    and mod 9, 36pq, and anti-τ numbers.
  - It does **not** discuss Theorem 22, the counting conjecture or π(n), and
    it does **not** cite Lauer 2014.
  - It is the only document in ETERA's full-text index that contains
    "Zelinsky" together with "refactorable", "taastegurdatav", or "Kennedy
    Cooper tau".

### Where I looked (all 2026-10-30)

- **ETERA** (etera.ee), Tallinn University's repository, through its own
  `/api/browse` Solr backend. The web UI is JavaScript-only and search engines
  do not index it.
  - Creator field "Lauer": 2 records, neither is the thesis. "Lauer, Helena": 0.
  - Full text (`##scontent`): "refactorable" (1 hit, Saar), "taastegurdatav"
    (1, Saar), "τ-arvude" (8, of which only Saar is relevant), "Zelinsky"
    (71, of which only Saar is relevant), "Colton" (84, likewise).
  - Note that ETERA holds many TLU student theses, but not all of them.
    Pre-2015 coverage is unknown.
- **ESTER** (ester.ee), the Estonian union library catalogue, which includes
  the TLÜ Academic Library.
  - Author "Lauer, Helena": not found. The neighbouring headings list no Helena.
  - Keywords "Lauer arvud" and "Lauer magistritöö": nothing relevant. The only
    Lauer theses are by Eda Lauer (Tartu 2014, education) and Liisi Lauer (EKA
    2009, architecture).
  - "τ-arvud" and "tau-arvud": 0.
- **ETIS** (Estonian research information system). The CV page for Mart Abel
  is JavaScript-rendered and its public API ignored my keyword searches. Not
  usable from here.
- **OpenAlex.** Two "Helena Lauer" author records, one at Tallinn University
  (1 work, ALR 2021). There is no thesis record. Zelinsky 2002 still has
  exactly one citing work, ALR.
- **Web search**, standard and extended, in English and Estonian: "Overview of
  τ-numbers"; "Helena Lauer" with τ-arvud, tau-arvud, magistritöö; Mart Abel as
  supervisor for 2014; site-restricted to etera.ee, tlu.ee, digar.ee,
  dspace.ut.ee and ester.ee. Nothing found.
- **Not tried, by the terms of the brief:** asking Abel, Redi or Lauer by
  e-mail. ALR print helena.lauer@mail.com and eredi@tlu.ee. Asking the TLÜ
  library for the paper copy is the only remaining route, and whether to use it
  is Aaron's decision.

## Dusart (6.5) against the published Ramanujan J. version (lit-colton-dusart, 2026-10-30)

Brief from `dev`: check the inequality pair the threshold proof cites
(`findings/colton-threshold.md` on `lead-colton` @ 5939dae, §0) against the
refereed published paper. The pair is

  (x/ln x)(1 + 1/ln x) ≤ π(x) for real x ≥ 599,
  π(x) ≤ (x/ln x)(1 + 1.2762/ln x) for real x > 1.

The threshold proof uses both halves.

### Verdict

**I could not read the published paper. The statement is not confirmed
against it.** Here is what I can say.

1. **Identical statement in the published version: CANNOT TELL from a
   primary source.** One secondary source attributes exactly this pair, with
   these ranges (x ≥ 599, x > 1), to the published Ramanujan J. 2018 paper,
   but gives no theorem number (item S1 below). Nothing I found says the pair
   was changed or dropped in publication. Nothing says it survived either,
   other than S1.
2. **Published numbering: NOT ESTABLISHED.** The secondary sources disagree
   and none of them numbers this pair. Axler cites "[Dusart 2018, Corollary
   5.2]" for the sibling bound (1 + 1/ln x + 2/ln²x) ≤ π(x), x ≥ 88,783
   (S2). That is the lower half of arXiv (6.7), the same Theorem 6.9. So the
   arXiv Theorem 6.9 material is probably in §5 of the published paper,
   possibly Corollary 5.2. That is an inference, not a reading. Wikipedia
   says "Theorem 5.1" for the 88,783 bound (S4), and it misprints the page
   range, so it is weak evidence.
3. **Erratum: no published erratum found.** Crossref has no `update-to` or
   correction record for the DOI. There is an **author-hosted correction**,
   READ, but it does not touch π(x) (P2).
4. **One known soundness issue upstream, since repaired. It does not affect
   the pair.** Broadbent et al. (Math. Comp. 2021, p. 2299) found that the
   main theorem of Ramaré's zero-density estimate, used in Dusart 2018, is
   incorrect. That puts Dusart 2018 Table 1 (the ψ bounds) in doubt. Axler
   2024, Proposition 2, recovers every line of Table 1 from Broadbent et al.
   and Fiori–Kadiri–Swidinsky (S3, READ). I trace this chain only through
   Axler.
   - It matters only if the published proof of the pair leans on Table 1.
     In the arXiv proof (P1), (6.5) follows from (6.7) for large x. (6.7)
     needs only |θ(x) − x| ≤ η_k x/ln^k x for x ≥ 10¹¹, with η₂ = 0.05 and
     η₃ = 6, plus "direct computation for small values". Those θ bounds are
     far weaker than what Broadbent et al. now prove independently.
   - I have not checked that reduction. It is a reason the pair is unlikely
     to be wrong, not a proof.

**What would have to be true for this verdict to be wrong:** the published
paper changes the constant 1.2762 or the threshold 599, or drops the pair.
Then the threshold proof's citation would point at the arXiv preprint only.
S1 is the only evidence against that, and it is one secondary source.

**Practical recommendation, not a finding:**
- Cite the pair as Dusart, arXiv:1002.0442v1, Theorem 6.9, eq. (6.5), READ.
  That is what the finding already does.
- Add "also attributed to Ramanujan J. 45 (2018) 227–251, not read". Do not
  cite a published theorem number until someone reads the paper.
- The pair is older than 2010. Axler (S2) and the arXiv text trace it to
  Dusart's 1998 thesis (Théorème 1.10) and to C. R. Math. Rep. Acad. Sci.
  Canada 21 (1999) 53–59. The 1999 paper is refereed. If the citation has to
  be to a refereed source, that paper may be the cheaper route than
  Springer. Its link on Dusart's page returned 404 (below), so I have not
  read it either.

### Sources

**Primary (Dusart):**

- **P0.** P. Dusart, "Explicit estimates of some functions over primes",
  Ramanujan J. **45** (2018), no. 1, 227–251. Online 2016-10-27. DOI
  10.1007/s11139-016-9839-4. zbMATH 1426.11088. NOT READ: paywalled.
  - The published title and abstract differ from arXiv v1 ("Estimates of
    some functions over primes without R.H."). The published abstract leads
    with an extended zero-free region. So the paper was revised, and arXiv
    numbering cannot be assumed to carry over.
  - arXiv has only v1, with no journal-ref (abs page checked 2026-10-30).
- **P1.** arXiv:1002.0442v1, Theorem 6.9, eq. (6.5), page 9, with its
  proof. READ 2026-10-30. The statement matches the finding character for
  character, including the note "1.2762 is chosen for x = p₂₅₈ = 1627".
- **P2.** Dusart, "correctif" to the Ramanujan J. paper, author-hosted at
  `unilim.fr/pages_perso/pierre.dusart/Recherche/correctif_RJ.pdf`. It is
  linked as "[ Correctif ]" beside P0 on his Publications page. Revision
  26/02/2018, 2 pages, sha256 bcd8b986…4d5d. READ 2026-10-30.
  - Its header still carries the old preprint title.
  - Thomas Morrill could not reproduce Table 1, and Dusart found "two typing
    errors in the published theorem". He restates published **Theorem 3.5**
    (the explicit bound for |ψ(x) − x|/x) and gives PARI code reproducing two
    Table 1 entries.
  - It says nothing about π(x). It is not a journal erratum.
  - Incidental: this confirms the published paper has a Theorem 3.5 and a
    Table 1.

**Secondary:**

- **S1.** "Inequalities involving arithmetic functions", arXiv:2404.17165
  (Lith. Math. J. 2024, DOI 10.1007/s10986-024-09655-x), survey §, p. 8.
  READ 2026-10-30, arXiv version.
  - It attributes the 1.2762 pair, "left inequality for x ≥ 599, right for
    x > 1", to its ref. [56] = Dusart, Ramanujan J. 45 (2018).
  - In the same breath it gives the 2.53816 pair with lower range x ≥
    **88,789**. Axler says 88,783 and arXiv (6.7) says 88,783, so this
    survey's transcription is not exact everywhere. The 88,783/88,789 bound
    is not used by the threshold proof.
- **S2.** C. Axler, "Estimates for π(x) for large values of x and
  Ramanujan's prime counting inequality", INTEGERS 18 (2018) #A61, p. 3.
  READ 2026-10-30.
  - "Dusart [7, p. 55] found that g₁(2) = 599. In [10, Corollary 5.2], he
    improved his own result by showing that g₁(3) = 88 783."
  - [7] is the 1999 C. R. Math. Rep. paper and [10] is P0. g₁(2) = 599 is
    exactly the lower half of the pair.
  - The arXiv version (1703.02407) instead cites [7, Théorème 1.10], the 1998
    thesis.
- **S3.** C. Axler, INTEGERS 24 (2024) #A34, pp. 6–7. READ 2026-10-30.
  - Records the Broadbent et al. objection to [30] = P0, Table 1.
  - Proposition 2: "The explicit values for ε given in [30, Table 1] are
    correct."
  - Proposition 3 recovers [30, Corollary 4.5] via [30, Proposition 4.4].
- **S4.** Wikipedia, "Prime-counting function", raw source 2026-10-30. READ.
  It says "(Theorem 5.1)" for the 88,783 / 7.59 bounds and misprints the
  pages as 225–234. Weak.
- **S5.** zbMATH 1426.11088, review by M. Hassani. READ 2026-10-30. It lists
  the paper's headline results (ψ, θ, p_n, π(x) with 0.53816 for x ≥ 11813,
  Mertens) and does not mention the 1.2762 pair.

### Where I looked for the published text (all 2026-10-30)

- **Springer article page.** "Buy article PDF USD 39.95". The content/pdf URL
  returns the HTML paywall, not a PDF.
- **Unpaywall:** `is_oa: false`, no repository copy.
- **Semantic Scholar:** openAccessPdf CLOSED.
- **Crossref:** no update-to or erratum relation.
- **HAL:** no record for this paper.
- **ResearchGate:** HTTP 403.
- **Author's Limoges pages.**
  - Publications.html links only to Springer and the correctif.
  - The `Recherche/` directory index returns 403.
  - The C. R. Math. Rep. 1999 link (`journals.cms.math.ca/CR/Vol_21/No_2.pdf`)
    returns 404.
- **Web search,** standard and extended, for the constants, the corollary
  numbers and the 1999 paper's title.
- **Not tried:** MathSciNet (no access), institutional library access, or
  e-mailing the author. The brief rules out contacting anyone. Buying the
  PDF or requesting it is Aaron's decision.

## Rosser–Schoenfeld 1962, Theorem 1: READ (lit-colton-rs62, 2026-10-31)

Brief from `dev`: read RS62 Theorem 1, the π(x) bounds. Report its exact
statement, constants, ranges and any later correction. This is the input
`adversary/colton.md` §5 proposes in place of Dusart (6.5), with the
analytic chain starting at 10⁹.

### Verdict

**READ, 2026-10-31.** Theorem 1 says exactly what `adversary/colton.md` §5 and
`adversary/colton/robust.py` assume: α = ½ with X₀ = 59, and γ = 3/2 for
x > 1. Both inequalities are strict, and log is the natural logarithm. No
correction to Theorem 1 was found in the authors' own follow-ups or anywhere
else I searched.

**Verbatim, from p. 69 of the journal scan (Illinois J. Math. 6 (1962),
§3 "Widely applicable approximations"):**

> THEOREM 1. *We have*
>
> (3.1)  (x / log x)(1 + 1/(2 log x)) < π(x)   *for* 59 ≤ x,
>
> (3.2)  π(x) < (x / log x)(1 + 3/(2 log x))   *for* 1 < x.

The same page also has these, given for context only:

> THEOREM 2. (3.3) x/(log x − ½) < π(x) for 67 ≤ x; (3.4) π(x) < x/(log x − 3/2) for e^{3/2} < x (and hence for 4.48169 ≤ x).
>
> COROLLARY 1. (3.5) x/log x < π(x) for 17 ≤ x; (3.6) π(x) < 1.25506 x/log x for 1 < x.

e^{3/2} = 4.48169 confirms that log means ln.

**What would have to be true for this to be wrong:**
- the scan I read differs from the printed journal (it is the Project Euclid
  scan of the printed pages, so this is very unlikely); or
- a correction exists somewhere I did not search: MathSciNet, or a paper that
  cites RS62 and that I did not read (717 Crossref citations).

### How Theorem 1 is proved (§7, p. 82, READ)

This is not a re-derivation. It records what the theorem rests on.

- **(3.2), the upper bound:**
  - x ≤ 16,000: the Rosser–Walker tabulation.
  - Up to 10⁸: Lemma 1 with Theorem 16, which is computational: tables to
    10⁷ and Baker–Gruenberger to ~10⁸, §5.
  - 10⁸ ≤ x ≤ e³⁷⁵: Lemma 2 with Theorem 29 (θ bounds).
  - Beyond e³⁷⁵: Lemma 3 with Theorem 31.
- **(3.1), the lower bound:** not proved directly. It is derived from (3.3)
  by the elementary inequality (x/log x)(1 + a/log x) < x/(log x − a) for
  eᵃ < x, with a = ½.
  - (3.3) is proved by Lemma 4 with Theorem 16 for x ≤ 10⁸, and by Lemma 5
    with Theorem 31 above that.
  - (3.3) starts at 67, so 59 ≤ x < 67 must come from a direct check. The
    paper's general remark on p. 69 covers this ("verified by reference to
    Lehmer's table"). It does not spell out that range for (3.1).
- **The analytic input is unconditional.** §6 (p. 78): "the first 25000
  zeros of the zeta function have real part equal to 1/2, as shown in
  Lehmer [8] and Lehmer [9]". That gives A = e^{9.99} in Rosser 1941's
  machinery, together with the zero-free region of Theorem 26.
  - No RH assumption is used.
  - Lehmer's 25,000 zeros lie far inside every later verification, e.g.
    3,502,500 in RS75 and Platt–Trudgian 2021. That input is not in doubt.

**For the Colton chain, starting at 10⁹:** the part of RS62 being leaned on
is the analytic range x ≥ 10⁸ (Lemmas 2, 3 and 5; Theorems 29 and 31). The
table-dependent range below 10⁸ is not used, and it is in any case covered
by the team's own exact range to 10⁹ (PR #28).

> **CORRECTION, 2026-10-31 (`lit-colton-rs62-note`).** The paragraph above
> is **wrong for (3.1)**. It is still right for (3.2). The old text stays
> as written so the record shows what was said.
>
> - **What the chain uses.** `lead-colton-rs62`'s chain (branch
>   `lead-colton-rs62` @ 81ad7d7, `findings/colton-threshold-rs62.md` §5,
>   read 2026-10-31) applies (3.2) only at x = n ≥ 10⁹. That is inside
>   RS62's analytic range.
> - It applies (3.1) at x = n/a for every a ∈ S. Its lowest stage starts at
>   x = 10⁹/110,000 = 9,090.9… So the chain leans on (3.1) over
>   [9,090.9, 10⁸). In RS62 that range is tabular, not analytic. I checked
>   the findings file's lower-end table against its stated ranges and max S.
> - **"Covered by the team's exact range to 10⁹ (PR #28)" was also wrong.**
>   PR #28's range checks Colton's inequality for n ≤ 10⁹. It does not check
>   (3.1) at real x < 10⁸, which is the input the chain uses for n > 10⁹.
>   What covers (3.1) there is a separate computation, `rs62-lower.txt`
>   (findings §5). I did not audit that computation.
>
> **How RS62 prove (3.1) below 10⁸.** I re-read pp. 69, 72, 75, 76, 81 and
> 82 as page images, from the same Wayback capture (sha256 `8e37b06f…`
> re-verified 2026-10-31).
>
> - **The statement has no qualification.** (3.1) is stated on p. 69 as
>   Theorem 1 "for 59 ≤ x". There is no footnote, no "assuming the
>   tables", and no error allowance. The dependence on computation shows
>   only in §§5–7.
> - **59 ≤ x ≤ 16,000: a direct tabulation.** p. 76: "The second major
>   computation … was the tabulation by Rosser and Walker of many functions
>   of primes for x ≤ 16,000. This verified Theorems 1–10 and their
>   corollaries in this range". Section 1 places it on the IBM 650 at
>   Cornell, about four years before publication.
> - **16,000 < x ≤ 10⁸: Lemma 4 with Theorem 16, then the elementary step.**
>   p. 82: "we combine Lemma 4 and Theorem 16 to verify (3.3) for x ≤ 10⁸",
>   and "We get (3.1) from (3.3) … by applying the inequality
>   (x/log x)(1 + a/log x) < x/(log x − a) for eᵃ < x" with a = ½.
>   - **Lemma 4 (p. 81) is analytic.** For e⁵ ≤ x,
>     x/(log x − ½) < li(x) − li(x^{1/2}). It is proved by comparing
>     derivatives and checking the lower limit x = e⁵ numerically, using
>     the W.P.A. Ei tables [18] for x ≤ e¹⁵.
>   - **Theorem 16, (4.1) (p. 72), is computational.** li(x) − li(x^{1/2})
>     < π(x) for 11 ≤ x ≤ 10⁸. Its proof (pp. 75–76) is three computations:
>     - Rosser checked it to 10⁶ from D. N. Lehmer's printed table of
>       primes [10]. The method is in Rosser 1941 [12].
>     - The first major computation (National Bureau of Standards / INA,
>       about nine years before publication) extended it to 10⁷.
>     - The Appel–Rosser tabulation for x ≤ 10⁸ "established Theorems 16
>       and 18–23 for 313 ≤ x ≤ 10⁸, which completed their verification".
>       This is the third computation, done at IDA, Project FOCUS.
> - **So everything (3.1) does below 10⁸ rests on 1950s–1961 machine
>   tabulations.** Above 16,000 that means Theorem 16 to 10⁸.
>   - The paper does not describe how a tabulation at finitely many points
>     certifies an inequality for every real x, or what rounding control
>     was used. It defers to the Appel–Rosser report [19]: K. I. Appel and
>     J. B. Rosser, *Table for estimating functions of primes*, IDA-CRD
>     Technical Report No. 4, September 1961, "available on request" from
>     IDA.
>   - **NOT READ.** One standard web search (2026-10-31) found only
>     citations, no scan or repository copy. A contemporary review exists,
>     Math. Comp. 16 (1962) pp. 500–501, RMT 55. I have not read it either.
>   - The Rand table of primes to ~10⁸ (Baker–Gruenberger [1], microcards)
>     is mentioned on p. 75. The paper does **not** say that the Appel–Rosser
>     tabulation used it.
> - **Corrections.** None to this part was found in the searches listed under
>   "Later corrections" below. RS62 itself corrects a digit in Rosser 1941
>   (the 2.05282 of (4.5), p. 72), not anything in its own Theorem 16.
>
> **What this means for the chain:** [L] for (3.1) on [9,090.9, 10⁸) is a
> citation of a refereed theorem. Over that range the theorem's own proof is
> a 1961 computation whose report the team cannot obtain. That is weaker
> than the analytic range, though not wrong. The chain does not need it if
> `rs62-lower.txt` stands as [C]. Findings §5 already uses it that way, and
> that is the right shape. Whether the Theorem cites (3.1) "on its full
> stated range" or rests that range on `rs62-lower.txt` is the team's call.
> The literature supports either one, with the qualification above.

### Later corrections: none found to Theorem 1

- **RS75.** Rosser & Schoenfeld, "Sharper bounds for the Chebyshev functions
  θ(x) and ψ(x)", Math. Comp. 29 (1975) 243–269. **READ** (first page and
  every passage citing "R–S", 2026-10-31).
  - It calls itself "an up-to-date version of part of" RS62 and uses RS62
    (4.5), (4.6), (4.11), (4.12), (3.38) and Theorem 13 as inputs.
  - It reserves π(x) for a later paper. It does not restate, revise or
    retract Theorem 1.
  - Its one correction footnote (p. 243, "**") corrects p. 71 of **Rosser,
    Yohe & Schoenfeld 1969**, not of RS62. I checked the footnote anchor on
    the page image. This is easy to misattribute, because RS62 p. 71 also
    exists.
- **Schoenfeld 1976.** "Sharper bounds … II", Math. Comp. 30 (1976) 337–360.
  **READ**: searched for every citation of RS62 ([10]).
  - It cites RS62 but has no correction to it.
  - Its in-text footnote on p. 75 of the scan corrects its own (5.10) and
    (5.11).
- **Schoenfeld's 1976 corrigendum.** Math. Comp. 30 (1976) 900. **READ.**
  - It corrects RS75's abstract reference [17] and Schoenfeld 1976
    (Theorem 11, (7.4); p. 349).
  - Nothing in it touches RS62.
- **zbMATH 0122.05001** (review by S. Knapowski). **READ via the zbMATH API.**
  - It quotes Theorem 1 with exactly the constants and ranges above. That is
    an independent transcription, which agrees with mine.
  - No erratum is linked.
- **Crossref** (10.1215/ijm/1255631807): no `update-to` or correction
  relation; 717 citing works.
- **Web search** (standard, two queries) for errata or corrections to RS62:
  - Nothing found.
  - The secondary literature cites Theorem 1 and Corollary 1 as standing
    results.

### Limits

- **I did not check the proof.** I read the statement and the proof outline
  in §7, not the lemmas behind it:
  - Lemmas 1–5 (pp. 81–82);
  - Theorems 29 and 31;
  - the Rosser 1941 results they use.
  "Refereed since 1962 and re-used without reported error" is the evidence
  for the theorem's correctness. It is [L], not [T].
- **MathSciNet** (MR 25 #1139) was not reachable, so any MR-recorded erratum
  is unchecked.
- **The 59 ≤ x < 67 slice of (3.1)** rests on the paper's general "verified
  by Lehmer's table" remark, not on a stated check. That slice is irrelevant
  to a chain starting at 10⁹, and the team's exact range covers it anyway.
  `adversary/colton/bounds.py` reports the minimum lower-bound slack 0.17 at
  67.
  - **CORRECTION, 2026-10-31 (`lit-colton-rs62-note`):** the attribution in
    the bullet above is wrong. So is the same attribution in "How Theorem 1
    is proved" above.
    - The p. 69 "Lehmer's table" remark covers only the **corollaries** of
      §3.
    - The 59 ≤ x < 67 slice of Theorem 1 is covered explicitly on p. 76:
      the Rosser–Walker tabulation "verified Theorems 1–10 and their
      corollaries" for x ≤ 16,000.
    - "Rests on … not on a stated check" should read: rests on a stated
      tabulation, which the paper does not reproduce.
    - Note also that the "irrelevant to a chain starting at 10⁹" reasoning
      does not carry over to [9,090.9, 10⁸). See the correction under
      "For the Colton chain" above.

### Sources and how they were obtained (all 2026-10-31)

- **RS62.** J. B. Rosser & L. Schoenfeld, "Approximate formulas for some
  functions of prime numbers", Illinois J. Math. 6 (1962) 64–94,
  doi:10.1215/ijm/1255631807.
  - Project Euclid's direct PDF URLs return an Incapsula bot wall to
    scripts, as adv-colton also found.
  - Read from the Wayback Machine capture of Project Euclid's own PDF:
    `https://web.archive.org/web/20210413062807id_/https://projecteuclid.org/journals/illinois-journal-of-mathematics/volume-6/issue-1/Approximate-formulas-for-some-functions-of-prime-numbers/10.1215/ijm/1255631807.pdf`,
    31 pages, sha256 `8e37b06f82e09421bceb2502578c47b61469141f0287e6acedb70e01765ab556`.
  - Theorem 1 was read from the page image at 200 dpi, not from OCR.
    The PDF is not committed.
- **RS75, Schoenfeld 1976 II, and the corrigendum.** AMS returned 403 to
  scripts. Read from the Wayback captures of the ams.org PDFs (2015–2016):
  - S0025-5718-1975-0457373-7, sha256 `65bef67b…`;
  - S0025-5718-1976-0457374-X, sha256 `fc86db1d…`;
  - S0025-5718-1976-0457375-1, sha256 `93c573b3…`.
- **zbMATH Open API:** document 0122.05001.

### Recommendation (not a finding)

The citation can read: Rosser & Schoenfeld, Illinois J. Math. 6 (1962),
Theorem 1, eqs. (3.1)–(3.2), p. 69, READ 2026-10-31.

This removes the theorem's only paywalled input, provided `lead-colton`
adopts the adversary's §5 route. That route still needs what
`adversary/colton.md` §5 lists:
- certified moments of G(287,050);
- the rational check.
