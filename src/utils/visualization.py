import matplotlib.pyplot as plt

def bar(metric: dict, title: str, out: str):
    plt.figure(figsize=(6, 4))
    plt.bar(metric.keys(), metric.values())
    plt.title(title)
    plt.tight_layout()
    plt.savefig(out)
    plt.close()

def log_message_flow(agent_logs: list, filename="message_flow.png"):
    plt.figure(figsize=(8, 4))
    for i, msg in enumerate(agent_logs):
        sender = getattr(msg, "sender_id", msg.get("sender", "unknown"))
        receiver = getattr(msg, "receiver_id", msg.get("receiver", "unknown"))
        content = getattr(msg, "content", msg.get("content", {}))
        text = str(content)[:20] + "..."

        plt.plot([i, i], [0, 1], color='gray', linewidth=1.5)
        plt.text(i, 1.05, f'{sender}→{receiver}', ha='center', fontsize=8)
        plt.text(i, -0.05, text, ha='center', fontsize=7)

    plt.xticks([])
    plt.yticks([])
    plt.title("Message Flow")
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()


def log_alert(alerts: list, filename="alerts.txt"):
    with open(filename, "w") as f:
        for alert in alerts:
            f.write(alert + "\n")
