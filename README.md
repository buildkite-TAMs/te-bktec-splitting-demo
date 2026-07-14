# Test Engine Lab: Test splitting with `bktec` (pytest)

A hands-on lab showing the **second half** of Test Engine: using the
[Test Engine Client (`bktec`)](https://github.com/buildkite/test-engine-client)
to **split a test suite across parallel agents by historical timing**, so the
whole suite finishes in a fraction of the wall-clock time.

**Time:** ~15 min · **Level:** intermediate · **Agent:** Linux + Docker (`queue: aws`) · **Plan:** Pro/Enterprise

---

## What's in this repo

```
te-bktec-splitting-demo/
├── src/mathops.py              # trivial code under test
├── tests/                      # 15 tests across 4 files, each with a sleep()
│   ├── test_arithmetic.py      #   so bktec has real TIMING differences to
│   ├── test_strings.py         #   balance — not just test counts
│   ├── test_numbers.py
│   └── test_slow.py            # deliberately the slowest file
├── requirements.txt            # pytest + buildkite-test-collector
└── .buildkite/
    ├── pipeline.yml            # one step, parallelism: 4, runs bktec
    └── steps/run-bktec.sh      # installs bktec, runs tests through it
```

Unlike the collector demos (which just *upload* results), this repo **consumes**
that timing data to go faster. The key line in `pipeline.yml`:

```yaml
parallelism: 4
command: "./.buildkite/steps/run-bktec.sh"   # the script calls `bktec run`
```

`bktec run` reads `BUILDKITE_PARALLEL_JOB` / `BUILDKITE_PARALLEL_JOB_COUNT`
(set automatically by `parallelism`), asks Test Engine for *this node's slice*
of the suite, and runs only those tests.

---

## Lab steps

### 1. Create the Test Engine suite

Test Engine → **New suite** → name `bktec-splitting-demo`, framework **pytest**.
(bktec needs a suite to read timing data from and upload results to.)

### 2. Give bktec an access token

bktec authenticates to the Test Engine API. This demo uses a **Buildkite API
access token** with scopes `read_suites`, `read_test_plan`, `write_test_plan`,
stored as the cluster secret **`TEC_API_TOKEN`** and exported to
`BUILDKITE_TEST_ENGINE_API_ACCESS_TOKEN` inside the step.

```bash
curl -H "Authorization: Bearer $TOKEN" \
  -X POST "https://api.buildkite.com/v2/organizations/tam-sandbox/clusters/<CLUSTER_ID>/secrets" \
  -H "Content-Type: application/json" \
  -d '{"key":"TEC_API_TOKEN","value":"<bktec access token>","policy":"- pipeline_slug: te-bktec-splitting-demo"}'
```

> 💡 **Production-preferred: keyless OIDC.** `bktec` v2.6.0+ auto-generates a
> temporary token via OIDC — no static secret at all. It's a great security
> talking point; we use a token here only to keep the demo self-contained.

### 3. Push and create the pipeline

Push to `git@github.com:buildkite-TAMs/te-bktec-splitting-demo.git` and create a
pipeline pointing at it.

### 4. Run a build and watch it split

Trigger a build. The step fans out into **4 parallel jobs**, each running a
*different* slice of the suite.

### ✅ Checkpoint

- The build is **green**, with **4 parallel jobs** under the one step.
- Each job's log shows `Running node N of 4` and runs only some of the tests.
- Total wall-clock time is well under running all 15 tests (~11s of sleeps) on
  one node.

---

## Stretch lab

- **Timing improves splitting.** The *first* build has no history, so bktec
  splits naively; after a run or two it balances by real timing. Run it 2–3
  times and watch the slow file (`test_slow.py`) get isolated so it's not stacked
  behind other slow tests.
- **Dial parallelism.** Bump `parallelism` to 8 and re-run. Does it keep getting
  faster? 🎯 Why not, once nodes outnumber meaningfully-splittable work? (bktec
  splits by *timing*, not count — diminishing returns is the real customer convo.)

---

## What you learned

- Test Engine isn't just observability — `bktec` **turns the collected timing
  data into faster builds**, with no test rewrites.
- Splitting is **by timing, not test count**, which is why it beats naive
  round-robin sharding.
- Auth can be **keyless (OIDC)** in production — a strong security story.

**Customer talking point:** "Your suite already uploads timing to Test Engine.
`bktec` uses it to split across agents and cut wall-clock time — and it can also
*mute quarantined flaky tests* at runtime so builds pass first try." (That second
half is the Workflows & quarantine lab.)
