# Colton's conjecture π(n) ≤ 2T(n): novelty sweep

*Literature scout `lit-colton-novelty`, 2026-10-31. I did none of the
mathematics. **READ** means I opened the primary text and found the statement
there. **CITED** means I saw it referenced and did not open it. I contacted
nobody and posted nothing. I ran this sweep before opening `literature/colton.md`,
as the brief asked. The comparison with that file is in §5.*

## Verdict

**PARTIALLY KNOWN.**

The full statement, π(n) ≤ 2T(n) for every n, has been **claimed proved since
2019-01-11**. The claim is in an OEIS entry that nobody links to:

> **OEIS A323326** (Jud McCranie), "a(n) = 2*T(n) - pi(n)". %C: *"Colton
> conjectured that T(n) >= pi(n)/2 for all n, i.e., this sequence is
> nonnegative. Zelinsky proved it for n > 7.42*10^13 (see the Zelinsky
> reference). This calculation went to 7.44*10^13, proving the conjecture."*
> READ 2026-10-31: the entry in text format, the data, and the full revision
> history.

| The team's result | Verdict | Basis |
|---|---|---|
| π(n) ≤ 2T(n) for all n (the statement) | **KNOWN as a claim.** McCranie, A323326, 2019: an exhaustive computation to 7.44·10¹³, combined with Zelinsky Thm 22. | READ. Unrefereed. No method, program or output is published. It rests on Zelinsky Thm 22 as a black box. |
| Equality only at n = 0 and n = 7 | **Partly known.** A323326's data shows a(7) = 0 and no other zero among its 123 displayed terms (n ≤ 123; minimum 2 for 8 ≤ n ≤ 123). Zelinsky notes n = 7 is sharp. Nobody states "only at 0 and 7" for the whole range. | READ |
| Exact check of every n ≤ 10⁹ | **KNOWN, by a larger claimed computation.** A323326 claims every n ≤ 7.44·10¹³. Ours is the only one with code, a certificate trail, a second implementation and a referee. | READ |
| Threshold lowered from 7.42·10¹³ to 10⁷ (re-derived Zelinsky method) | **No prior work found. "Cannot tell" for one source.** Nobody I found improves, corrects or re-derives Zelinsky's threshold. The one gap is Lauer 2014 (§3), which is unread. | §4 |
| A proof that does not depend on Zelinsky Thm 22's unpublished numbers | **No prior work found.** McCranie's claim needs Thm 22. Ours replaces it. | §4 |
| Lean formalisation of the full statement | **No prior work found.** Lean has only formal-conjectures `colton_conjecture`, marked `research open`, with `native_decide` to n ≤ 500. | §2 |

**What the team can honestly claim.**

- **Not** "first proof of Colton's conjecture". That would repeat the
  October 2025 failure.
- **Reasonable:** "an independent, reproducible, refereed proof".
  - It lowers Zelinsky's threshold to 10⁷.
  - That removes the dependence on Thm 22's unpublished computations and on a
    7.4·10¹³ computation of which only one sentence is public.
- The threshold reduction is new **as far as searched** (§4). That is a
  "found nothing" verdict, not a positive one.

**What would make this verdict wrong.**

1. **Lauer's 2014 Tallinn MSc thesis**, "Overview of τ-numbers", CITED by
   Abel–Lauer–Redi 2021. It may re-derive or improve Thm 22. Neither I nor
   two earlier chats could obtain it.
2. **A McCranie write-up of the 2019 computation**, on a personal page or on
   SeqFan. If it exists, it might state its own threshold or method. The
   SeqFan archive (list.seqfan.eu) was **unreachable** from here.
3. **A citer of Zelinsky that OpenAlex misses.** Google Scholar and
   MathSciNet were not reachable.

## Method lesson

Search the OEIS **full text**, not just the entry the conjecture lives on.
Use the conjecture's name, its author, the citing paper's author, and each of
its counting functions. A result can sit in an **unlinked sibling sequence**.

Here the conjecture lives on A111291, and the settlement sits on A323326 (the
difference 2T(n) − π(n)). No %Y line connects them, and web search does not
index A323326, so a pass through the home entry plus web search cannot reach
it.

The query that found it was OEIS full-text search for `zelinsky tau`
(`https://oeis.org/search?q=zelinsky+tau&fmt=text`). It is also returned by
`refactorable prime`, by `tau numbers pi`, and by `colton` (result page 4
of 4, hits 31-40). For any OEIS-sourced problem, run those searches as a matter of course:
name of the conjecture, its author, and the paper that proved part of it.

## 1. The prior claim: OEIS A323326

- **Author and date.** Jud McCranie, revisions #1–#13, all on 2019-01-11.
  - Approved by Bruno Berselli (#10, #13).
  - Edits by Jon E. Schoenfield and Michel Marcus were formatting only. The
    one Discussion note is Marcus, "wrong section".
  - No editor asked how the calculation was done. READ (history page,
    2026-10-31).
- **Content.**
  - The comment quoted above.
  - Data starting 2, 3, 2, 2, 1, 1, **0**, 2, 4, 4, 3, …, so a(7) = 0.
  - %H links only to Colton 1999 and Zelinsky 2002.
  - No b-file: the b-file URL returns a file "synthesized from sequence entry".
  - No program and no %E.
- **Why everyone missed it.**
  - A111291, A033950 (rev #171, 2026-10-05) and A208251 (the T(n) entry,
    rev #32) carry **no %Y back-link** to A323326. I checked each entry's text
    for the string.
  - Neither web search engine I used indexes A323326. A quoted search for
    "A323326" returned nothing.
  - formal-conjectures, Wikipedia and MathWorld (updated 2026-10-30) do not
    mention it.
  - I found it only through the OEIS's own full-text search, "zelinsky tau".
- **How strong the claim is.**
  - It is one sentence by a well-known OEIS contributor with a long record of
    large computations (e.g. A114617's b-file to 94,342 terms).
  - It is not checkable: the method, the minimum of a(n) and the code are all
    unknown.
  - It inherits whatever is wrong with Zelinsky Thm 22. Thm 22 rests on
    unpublished counts (413,980 p-generators below 28,653,696, A > .508,
    B < 8,694,520,815) and on lemmas "left to the reader".
  - Its 7.44·10¹³ covers Thm 22's n > 7.42·10¹³ with a margin of 2·10¹¹.

## 2. Formal and AI work

- **formal-conjectures `FormalConjectures/OEIS/111291.lean`.** READ, clone
  pulled 2026-10-31. The history clone is shallow, so I used the GitHub API
  for the PRs.
  - Issue #5227 (tadamcz, 2026-08-31): `conjecture` was misformalised
    (∀ real x > 1, false on (1,2)). Fixed by PR #5233, merged 2026-09-09.
  - PR #5399 (mo271, merged 2026-09-11) marks the eventual form
    `research solved` and adds `colton_conjecture` as `research open`, citing
    "7.42·10¹³ … the remaining range is open". **This is out of date.** A323326
    had claimed the range closed seven years earlier. Correcting it upstream is
    outward-facing: Aaron's call.
  - PR #6644 (2026-09-27) adds the `a_4` test. `colton_conjecture_le_500`
    is `native_decide`.
  - Citation slip: the docstring's "[Ze02, Theorem 7]" is the TeX
    `\label{thm7}`. The printed number is **Theorem 14**. The 7.42·10¹³
    result is printed **Theorem 22**. I verified this by counting the shared
    theorem counter in the TeX source.
- **Kuberwastaken/c5-k4.** READ via the GitHub API, 2026-10-31.
  - It has a Lean disproof of the misformalised real-x statement at x = 3/2,
    explicitly "not a refactorable-number disproof".
  - It checks the weak x/(2 log x) form at every integer ≤ 10⁷. That is not
    the π form.
- **the-omega-institute/trureturing.** `SCREENED-OUT.md` and
  `TARGET-GATES.md` (READ) drop A111291 as "covered … by Zelinsky's 2002
  Theorem 14 … only a finite range remains". The project did not attempt it.
- **competemath/emissary-archangel.** It holds only an export of the old fc
  statements, with no proof.
- **AlphaProof Nexus** (Tsoukalas et al., arXiv:2605.22763, abstract READ)
  and **OEIS Open** (Adamczewski, arXiv:2608.11941, abstract READ) both use
  the same 492 OEIS problems.
  - The `epoch-research/LeanOpenProblems` tree (READ via API) has 492 files
    under `apn/data/oeis/Isolated`, and none is 111291.
  - Code search of `LeanOpenProblems-results` for 111291 found nothing.
  - So neither one attempted this problem.
- **Tao's AI-contributions wiki** (READ 2026-10-31) covers only Erdős
  problems. A111291 is not there.
- **Lean Zulip.** Code search of `leanprover-community/archive` for
  refactorable, "tau number", A111291 and Colton found only unrelated
  "refactor" threads.

## 3. Papers

- **Colton 1999**, JIS 2, 99.1.2: the origin of the conjecture. CITED here
  (READ in full by `lit-colton`).
- **Zelinsky 2002**, JIS 5, 02.2.8. READ, TeX source, 2026-10-31.
  - Printed Thm 14 is T(n) > kπ(n) eventually.
  - Printed Thm 22 is n > 7.42·10¹³.
  - The text says "a more general method … lower the bound to slightly over
    7·10¹³". It claims nothing lower.
- **Abel, Lauer & Redi 2021**, Acta Comment. Univ. Tartu. Math. 25(1),
  doi 10.12697/ACUTM.2021.25.07.
  - I READ the landing page and abstract only: τ-numbers relative to integer
    polynomials. Nothing in the abstract concerns π(n) ≤ 2T(n).
  - OpenAlex lists it as the **only** indexed citer of Zelinsky 2002.
  - Their finding that two other Zelinsky proofs are wrong is from
    `lit-colton`'s reading. I did not re-read the body.
- **Lauer 2014**, MSc thesis, Tallinn. CITED by ALR. Not obtained.
- **Zhang Zhonghua 2006**, "A note on the number of tau numbers" (CNKI
  SDXK200602007, OpenAlex W2385579128).
  - CITED only. The landing page failed on a TLS certificate mismatch.
  - OpenAlex records no reference to Zelinsky or Colton. The title suggests
    counting results, so it is a **small residual risk**: not read.
- **Spiro 1985** and **Cooper–Kennedy 1989/90** are asymptotic and density
  results. CITED. They give no finite threshold.
- **arXiv.** The API was unreachable from this box (HTTP 000). Web searches
  for refactorable or tau numbers with 2025–2026 papers surfaced none.
  - **Not a full arXiv search.** If the referee wants one, it should be
    rerun from a host that can reach export.arxiv.org.

## 4. What I searched (all 2026-10-31)

- **Local clones**, pulled first: erdosproblems, erdosproblems.wiki,
  formal-conjectures. I grepped for a111291, refactorable, tau.number and
  colton. Only fc's file matched. **Not an Erdős problem.**
- **OEIS.**
  - Entries: A111291 (rev #7, 2013), A033950 (rev #171), A208251, A323326 and
    its full history, plus the A111291 draft page.
  - Full-text searches: A111291, refactorable, "refactorable prime", Colton
    (all 40 hits scanned), Zelinsky, "zelinsky tau", "tau numbers pi",
    A323326.
- **formal-conjectures GitHub.** PRs and issues for 111291, refactorable,
  Colton and "tau number". I read #5227, #5233, #5399, #6644 and #4923.
- **GitHub.** Repo search: refactorable, "tau numbers", A111291, A323326,
  "Colton conjecture". Code search: A111291, A323326, OeisA111291,
  colton_conjecture, "refactorable primeCounting", "refactorable 7.42".
  Issue search: refactorable, "tau numbers".
- **StackExchange API.** MathOverflow and math.SE for refactorable, "tau
  numbers" and "tau number". Hits: MO 343399 (a different tau-number problem),
  MO 168855 (n/d(n)), MO answer 92148 (computer-discovered conjectures; could
  not be fetched to read) and MSE 3967536 (factors of refactorables). None
  concerns π(n) ≤ 2T(n) by title.
- **Zenodo API**: refactorable, "tau numbers", A111291, "Colton conjecture".
  Nothing relevant.
- **OpenAlex.** Search for refactorable and "tau numbers". Citers of Zelinsky
  2002 (W1654336639): 1. Citers of Colton 1999 (W3019648277): 54, all scanned
  by title. They are AI-discovery, philosophy-of-mathematics and graph
  conjecturing work, plus Raili Vilt's 2010 Estonian thesis on divisor-count
  sequences and ALR 2021. None is a threshold or range result.
- **Wikipedia** "Refactorable number" and **MathWorld** (READ). Neither
  mentions the π conjecture's status.
- **Web search**, standard and extended, on all names in the brief.
- **Unreachable:** arXiv API, SeqFan archive, CNKI, Google Scholar,
  MathSciNet, and MathOverflow pages by direct fetch.

## 5. Against the earlier pass (`literature/colton.md`, read after the above)

- **It missed A323326.** That is the finding that changes the verdict. Its
  sentence "No source claims the whole statement" is wrong, and so is its
  finite-range row ("NEW as far as searched").
  - The cause is structural: A323326 has no back-links, and web search does
    not index it.
  - It has been handled. I ticketed the team on finding it, and lead-colton
    has rewritten `findings/colton-conjecture.md` (PR #33) to claim no
    novelty for the statement or the finite range.
- **It found things I did not.**
  - The Lauer thesis chase (§8 there).
  - ALR's errata on Zelinsky, from reading the body.
  - Cloned AlphaProof Nexus results (38 OEIS outputs) and the `auto_oeis`
    branch provenance (PR #4450).
  - Colton's original text and the c5-k4 commit pins.
  - I did not repeat these, so they stand on its reading.
- **We agree on** the Thm 14 / Thm 22 numbering, the fc citation slip, the
  absence of any Lean proof, and OpenAlex's single Zelinsky citer.
- **Suggested edit to `literature/colton.md`,** for its owner: correct the
  finite-range and "no source claims" lines to cite A323326.

## 6. Not established

- Whether McCranie's computation was correct, or what minimum of a(n) it
  found above n = 7. Nobody can check it from what is public.
- Whether Lauer 2014 lowers or corrects Thm 22.
- A full arXiv listing search (API unreachable).

## 7. Follow-up asked by dev (2026-10-31): threshold, McCranie artefacts, citers of A323326

Nothing found. The verdict above stands.

- **Citers of A323326.**
  - OEIS full-text search for "A323326" returns only the entry itself and
    A332329. A332329 is a cos-x Maclaurin zero whose %Y lists "A323326"
    beside A323330/A323331, evidently a mis-typed neighbour. It is unrelated.
  - OpenAlex search for A323326: 0 works.
  - GitHub code search: only `loda-lang/loda-programs` `oeis/323/A323326.asm`.
    That is LODA's machine-mined program for the *sequence*, not the 7.44·10¹³
    computation (CITED from the search hit, not opened).
- **McCranie artefacts.**
  - The entry has no b-file; the b-file URL serves one "synthesized from
    sequence entry". It has no %o program and no %H to code.
  - His OEIS wiki user page (READ, last edited 2026-01-24) mentions
    totient/sigma projects and a ResearchGate Ulam-numbers report. It says
    nothing on tau numbers.
  - GitHub code search for "McCranie refactorable" and "7.44*10^13": nothing.
- **Threshold improvements.**
  - Zelinsky's own publication list (sites.google.com/view/joshuazelinsky,
    READ) has 15 items. The tau-numbers paper is the only one on the subject,
    with no erratum or follow-up.
  - An extended web search for explicit or improved bounds turned up nothing
    beyond Zelinsky 2002.
  - Still open: Lauer 2014 and an arXiv API search (unreachable). The
    remaining ask is a check from a host that can reach export.arxiv.org and
    the SeqFan archive.
