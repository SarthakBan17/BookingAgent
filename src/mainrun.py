import uuid
from graph import app

def print_stream(stream):
    for ns, update in stream:
        print(f"Namespace '{ns}'")
        for node, node_updates in update.items():
            if node_updates is None:
                continue

            if isinstance(node_updates, (dict, tuple)):
                node_updates_list = [node_updates]
            elif isinstance(node_updates, list):
                node_updates_list = node_updates
            else:
                raise ValueError(node_updates)

            for node_updates in node_updates_list:
                print(f"Update from node '{node}'")
                if isinstance(node_updates, tuple):
                    print(node_updates)
                    continue
                messages_key = next(
                    (k for k in node_updates.keys() if "messages" in k), None
                )
                if messages_key is not None:
                    node_updates[messages_key][-1].pretty_print()
                else:
                    print(node_updates)

        print("\n\n")

    print("\n===\n")



config = {"configurable": {"thread_id": str(uuid.uuid4()), "user_id": "1"}}


while True:
    try:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        print_stream(
            app.stream(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": user_input,
                        }
                    ]
                },
                config,
                subgraphs=True,
            )
        )
    except:
        # fallback if input() is not available
        print_stream(
            app.stream(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": "i am looking for a flight from boston to ny tomorrow",
                        }
                    ]
                },
                config,
                subgraphs=True,
            )
        )
        break