#!/usr/bin/env bash
# Install bktec + pytest, then run the tests THROUGH bktec so it splits them
# across this build's parallel jobs by historical timing.
#
# This is a committed script (not inline in pipeline.yml) so plain single-$
# variables are safe — pipeline upload doesn't interpolate script contents.
set -euo pipefail

echo "--- :package: Installing bktec (Buildkite apt registry) + pytest"
apt-get update -qq && apt-get install -y -qq --no-install-recommends curl gpg >/dev/null
install -d /etc/apt/keyrings
curl -fsSL "https://packages.buildkite.com/buildkite/test-engine-client-deb/gpgkey" \
  | gpg --dearmor -o /etc/apt/keyrings/buildkite_test-engine-client-deb-archive-keyring.gpg
echo "deb [signed-by=/etc/apt/keyrings/buildkite_test-engine-client-deb-archive-keyring.gpg] https://packages.buildkite.com/buildkite/test-engine-client-deb/any/ any main" \
  > /etc/apt/sources.list.d/buildkite-test-engine-client.list
apt-get update -qq && apt-get install -y -qq bktec >/dev/null
pip install --quiet -r requirements.txt

# bktec auth: this demo uses a scoped Buildkite API access token (stored as the
# cluster secret BKTEC_API_TOKEN). In production, prefer keyless OIDC — bktec
# v2.6.0+ generates a temporary token automatically, no static secret needed.
export BUILDKITE_TEST_ENGINE_API_ACCESS_TOKEN="${BKTEC_API_TOKEN:-}"

echo "--- :test_engine: Running node ${BUILDKITE_PARALLEL_JOB:-0} of ${BUILDKITE_PARALLEL_JOB_COUNT:-1} via bktec"
bktec run
