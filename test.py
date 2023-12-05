from data import Message, CompassMessage

original_data = CompassMessage("ID", 1, 2, 3)
serialized = original_data.serialize()

sent = len(serialized).to_bytes(2, "big") + serialized

sent_len = int.from_bytes(sent[:2], "big")
sent_data = sent[2:sent_len + 2]

deserialized: CompassMessage = Message.deserialize(sent_data)

print(deserialized.id)
print(deserialized.x)
print(deserialized.y)
print(deserialized.z)