#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${ROOT_DIR}"

export PATH="$HOME/.local/bin:$HOME/.local/google-cloud-sdk/bin:$PATH"

# Use Application Default Credentials access token if available so reauth prompts are avoided
if [[ -z "${CLOUDSDK_AUTH_ACCESS_TOKEN:-}" ]]; then
  ADC_TOKEN="$(gcloud auth application-default print-access-token 2>/dev/null || true)"
  if [[ -n "${ADC_TOKEN}" ]]; then
    export CLOUDSDK_AUTH_ACCESS_TOKEN="${ADC_TOKEN}"
  fi
fi

SERVICE_NAME="${SERVICE_NAME:-circana-alpha-evolve-pdi}"
PROJECT_ID="${1:-${PROJECT_ID:-$(gcloud config get-value project 2>/dev/null || echo "shade-sandbox")}}"
REGION="${2:-${REGION:-us-central1}}"

if [[ -z "${PROJECT_ID}" || "${PROJECT_ID}" == "(unset)" ]]; then
  echo "❌ Error: GCP Project ID not specified."
  echo "Usage: ./deploy.sh <YOUR_GCP_PROJECT_ID> [REGION]"
  exit 1
fi

echo "🚀 Deploying ${SERVICE_NAME} to Google Cloud Run..."
echo "   • Project: ${PROJECT_ID}"
echo "   • Region:  ${REGION}"

gcloud run deploy "${SERVICE_NAME}" \
  --quiet \
  --source . \
  --project "${PROJECT_ID}" \
  --region "${REGION}" \
  --platform managed \
  --ingress all \
  --allow-unauthenticated \
  --no-invoker-iam-check \
  --memory 1Gi \
  --cpu 2 \
  --port 8080 \
  --timeout 300

gcloud run services add-iam-policy-binding "${SERVICE_NAME}" \
  --project "${PROJECT_ID}" \
  --region "${REGION}" \
  --member="allUsers" \
  --role="roles/run.invoker" >/dev/null 2>&1 || true

SERVICE_URL="$(gcloud run services describe "${SERVICE_NAME}" --project "${PROJECT_ID}" --region "${REGION}" --format 'value(status.url)')"
echo ""
echo "✅ Deployment Complete!"
echo "🌐 Live Cloud Run URL: ${SERVICE_URL}"
