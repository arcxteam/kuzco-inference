#!/bin/bash

BASE_DIR=$(pwd)
KUZCO_TEMPLATE="kuzco-inference"
ACTION=""
COUNT=0
START_ID=1
END_ID=1

print_usage() {
    echo "Usage:"
    echo "  Setup Workers:   $0 setup --count <num> --start-from-id <id>"
    echo "  Start Worker:    $0 start <id> OR $0 start <start_id>-<end_id>"
    echo "  Stop Worker:     $0 stop <id> OR $0 stop <start_id>-<end_id>"
    echo "  Restart Worker:  $0 restart <id> OR $0 restart <start_id>-<end_id>"
    echo "  Stop All:        $0 stop-all"
    echo "  Check Status:    $0 status <id> OR $0 status <start_id>-<end_id>"
    exit 1
}

setup_worker() {
    for ((i=0; i<COUNT; i++)); do
        ID=$((START_ID + i))
        INSTANCE_DIR="$BASE_DIR/kuzco-inference-$ID"

        if [[ -d "$INSTANCE_DIR" ]]; then
            echo "⚠️  Instance $INSTANCE_DIR already exists. Skipping..."
            continue
        fi

        echo "📁 Creating instance kuzco-inference-$ID..."
        mkdir -p "$INSTANCE_DIR"
        rsync -a --exclude='.ollama' "$KUZCO_TEMPLATE/" "$INSTANCE_DIR/"

        sed -i "s/home/kuzco-inference-$ID/g" "$INSTANCE_DIR/docker-compose.yaml"
        sed -i "s/WORKER_NAME:.*/WORKER_NAME: \"kuzco-inference-$ID\"/g" "$INSTANCE_DIR/docker-compose.yaml"

        # Generate machine-id
        cd "$INSTANCE_DIR" || exit
        dbus-uuidgen > machine-id

        mkdir -p .ollama
        chmod -R 777 .ollama

        echo "✅ Instance kuzco-inference-$ID created successfully!"
        cd "$BASE_DIR" || exit
    done
}

start_worker() {
    for ((ID=START_ID; ID<=END_ID; ID++)); do
        INSTANCE_DIR="$BASE_DIR/kuzco-inference-$ID"
        if [[ ! -d "$INSTANCE_DIR" ]]; then
            echo "❌ Error: Instance $INSTANCE_DIR not found! Skipping..."
            continue
        fi
        cd "$INSTANCE_DIR" || exit
        echo "🚀 Starting kuzco-inference-$ID..."
        docker-compose up -d --build
        echo "✅ kuzco-inference-$ID started!"
        cd "$BASE_DIR" || exit
    done
}

stop_worker() {
    for ((ID=START_ID; ID<=END_ID; ID++)); do
        INSTANCE_DIR="$BASE_DIR/kuzco-inference-$ID"
        if [[ ! -d "$INSTANCE_DIR" ]]; then
            echo "❌ Error: Instance $INSTANCE_DIR not found! Skipping..."
            continue
        fi
        cd "$INSTANCE_DIR" || exit
        echo "🛑 Stopping kuzco-inference-$ID..."
        docker-compose down
        echo "✅ kuzco-inference-$ID stopped!"
        cd "$BASE_DIR" || exit
    done
}

restart_worker() {
    for ((ID=START_ID; ID<=END_ID; ID++)); do
        INSTANCE_DIR="$BASE_DIR/kuzco-inference-$ID"
        if [[ ! -d "$INSTANCE_DIR" ]]; then
            echo "❌ Error: Instance $INSTANCE_DIR not found! Skipping..."
            continue
        fi
        cd "$INSTANCE_DIR" || exit
        echo "🔁 Restarting kuzco-inference-$ID..."
        docker-compose restart
        echo "✅ kuzco-inference-$ID restarted!"
        cd "$BASE_DIR" || exit
    done
}

stop_all_workers() {
    echo "🛑 Stopping all kuzco instances..."
    for dir in kuzco-inference-*; do
        if [[ -d "$dir" ]]; then
            cd "$dir" || continue
            echo "Stopping $dir..."
            docker-compose down
            cd "$BASE_DIR" || exit
        fi
    done
    echo "✅ All kuzco instances stopped!"
}

check_status() {
    ONLINE=()
    NOT_HEALTHY=()

    for ((ID=START_ID; ID<=END_ID; ID++)); do
        INSTANCE_DIR="$BASE_DIR/kuzco-inference-$ID"
        if [[ ! -d "$INSTANCE_DIR" ]]; then
            echo "⚠️  Instance kuzco-inference-$ID not found! Skipping..."
            continue
        fi

        cd "$INSTANCE_DIR" || continue
        LOG=$(docker-compose logs --tail 100 2>/dev/null)

        if echo "$LOG" | grep -q "Heartbeat complete"; then
            ONLINE+=("worker $ID")
        else
            NOT_HEALTHY+=("worker $ID")
        fi
        cd "$BASE_DIR" || exit
    done

    echo -e "\n✅ Online:"
    for worker in "${ONLINE[@]}"; do
        echo "  - $worker"
    done

    echo -e "\n⚠️ Not Healthy:"
    for worker in "${NOT_HEALTHY[@]}"; do
        echo "  - $worker"
    done
}

parse_range() {
    if [[ "$1" =~ ^[0-9]+-[0-9]+$ ]]; then
        START_ID=$(echo "$1" | cut -d'-' -f1)
        END_ID=$(echo "$1" | cut -d'-' -f2)
    else
        START_ID=$1
        END_ID=$1
    fi
}

# Argument parsing
case "$1" in
    setup)
        while [[ $# -gt 0 ]]; do
            case "$2" in
                --count)
                    COUNT="$3"
                    shift 2
                    ;;
                --start-from-id)
                    START_ID="$3"
                    shift 2
                    ;;
                *)
                    break
                    ;;
            esac
        done
        if [[ $COUNT -eq 0 ]]; then print_usage; fi
        setup_worker
        ;;
    start)
        if [[ -z "$2" ]]; then print_usage; fi
        parse_range "$2"
        start_worker
        ;;
    stop)
        if [[ -z "$2" ]]; then print_usage; fi
        parse_range "$2"
        stop_worker
        ;;
    restart)
        if [[ -z "$2" ]]; then print_usage; fi
        parse_range "$2"
        restart_worker
        ;;
    stop-all)
        stop_all_workers
        ;;
    status)
        if [[ -z "$2" ]]; then print_usage; fi
        parse_range "$2"
        check_status
        ;;
    *)
        print_usage
        ;;
esac
