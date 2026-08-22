#!/usr/bin/env bash
set -euo pipefail

# PEFY Agentic Dev Fabric bootstrap
# - installs or updates the official 21st.dev CLI
# - installs 21st.dev agent skills
# - initializes 21st MCP for detected supported clients
# - installs Agency Agents using the repository's native installer
#
# Secrets are never written by this script. Set API_KEY_21ST in the shell that
# launches your coding client, or allow 21st login to handle local auth.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
UPDATE="${PEFY_DEV_UPDATE:-1}"
ALLOW_INTERACTIVE_AUTH="${PEFY_ALLOW_INTERACTIVE_AUTH:-0}"
INSTALL_AGENCY="${PEFY_INSTALL_AGENCY:-1}"
FORCE_CLIENTS="${PEFY_FORCE_21ST_CLIENTS:-}"

log()  { printf '[PEFY] %s\n' "$*"; }
warn() { printf '[PEFY][WARN] %s\n' "$*" >&2; }
die()  { printf '[PEFY][ERR] %s\n' "$*" >&2; exit 1; }

command_exists() { command -v "$1" >/dev/null 2>&1; }

require_node18() {
  command_exists node || die "Node.js 18+ is required."
  local major
  major="$(node -p 'Number(process.versions.node.split(".")[0])')"
  [[ "$major" -ge 18 ]] || die "Node.js 18+ is required. Found $(node --version)."
  command_exists npm || die "npm is required."
  command_exists npx || die "npx is required."
}

install_21st_cli() {
  if command_exists 21st; then
    if [[ "$UPDATE" == "1" ]]; then
      log "Updating 21st.dev CLI"
      npm install -g @21st-dev/cli@latest
    else
      log "21st.dev CLI already present"
    fi
  else
    log "Installing 21st.dev CLI"
    npm install -g @21st-dev/cli@latest
  fi
}

install_21st_skills() {
  log "Installing official 21st.dev agent skills"
  21st install-skill
}

client_detected() {
  case "$1" in
    codex)     command_exists codex ;;
    claude)    command_exists claude ;;
    cursor)    command_exists cursor ;;
    vscode)    command_exists code ;;
    windsurf)  command_exists windsurf ;;
    *)         return 1 ;;
  esac
}

client_forced() {
  [[ -n "$FORCE_CLIENTS" ]] || return 1
  case ",${FORCE_CLIENTS}," in
    *",$1,"*) return 0 ;;
    *) return 1 ;;
  esac
}

init_21st_client() {
  local client="$1"
  if ! client_detected "$client" && ! client_forced "$client"; then
    return 0
  fi

  if [[ -z "${API_KEY_21ST:-}" && "$ALLOW_INTERACTIVE_AUTH" != "1" ]]; then
    warn "Skipping 21st MCP init for $client because API_KEY_21ST is not set. Set it or use PEFY_ALLOW_INTERACTIVE_AUTH=1."
    return 0
  fi

  log "Initializing 21st MCP for $client"
  if ! 21st init --client "$client"; then
    warn "21st init failed for $client. Continue with remaining clients."
  fi
}

install_agency_agents() {
  [[ "$INSTALL_AGENCY" == "1" ]] || return 0
  [[ -x "$ROOT_DIR/scripts/convert.sh" ]] || die "scripts/convert.sh is missing or not executable."
  [[ -x "$ROOT_DIR/scripts/install.sh" ]] || die "scripts/install.sh is missing or not executable."

  log "Refreshing Agency Agents integrations"
  (cd "$ROOT_DIR" && ./scripts/convert.sh)

  log "Installing detected Agency Agents in parallel"
  (cd "$ROOT_DIR" && ./scripts/install.sh --no-interactive --parallel)
}

main() {
  require_node18
  install_21st_cli
  install_21st_skills

  local client
  for client in codex claude cursor vscode windsurf; do
    init_21st_client "$client"
  done

  install_agency_agents

  log "Bootstrap complete"
  if [[ -z "${API_KEY_21ST:-}" ]]; then
    warn "21st.dev authentication is not active in this shell. Export API_KEY_21ST before launching your coding client, or run '21st login'."
  fi
  log "Recommended next check: run the target project's lint, typecheck, tests, and UI smoke checks."
}

main "$@"
