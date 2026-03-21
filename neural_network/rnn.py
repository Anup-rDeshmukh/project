import torch
import torch.nn as nn
import torch.optim as optim
import re
import csv


texts = []
labels = []

with open("sms_sample.csv", "r", encoding="utf-8") as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        message = row.get("message", "").strip()
        category = row.get("category", "").strip()
        if message and category:
            texts.append(message)
            labels.append(category)


def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    return text

texts = [clean_text(t) for t in texts]


tokenized = [t.split() for t in texts]


vocab = {}
idx = 1  

for sentence in tokenized:
    for word in sentence:
        if word not in vocab:
            vocab[word] = idx
            idx += 1


def encode(sentence):
    return [vocab[word] for word in sentence]

encoded = [encode(s) for s in tokenized]



max_len = max(len(seq) for seq in encoded)

def pad(seq):
    if len(seq) >= max_len:
        return seq[:max_len]
    return seq + [0] * (max_len - len(seq))

padded = [pad(s) for s in encoded]


label_map = {label: idx for idx, label in enumerate(sorted(set(labels)))}
y = torch.tensor([label_map[l] for l in labels])



X = torch.tensor(padded)



class RNNModel(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_size, num_classes):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.rnn = nn.RNN(embed_dim, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        x = self.embedding(x)          # (batch, seq_len, embed_dim)
        out, _ = self.rnn(x)           # (batch, seq_len, hidden)
        out = out[:, -1, :]            # last time step
        out = self.fc(out)
        return out


model = RNNModel(
    vocab_size=len(vocab)+1,
    embed_dim=8,
    hidden_size=16,
    num_classes=len(label_map)
)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)


for epoch in range(50):
    outputs = model(X)
    loss = criterion(outputs, y)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    print(f"Epoch {epoch+1}, Loss: {loss.item():.4f}")


def predict(text):
    text = clean_text(text)
    tokens = text.split()
    
    encoded = [vocab.get(word, 0) for word in tokens]  # unknown → 0
    padded_seq = pad(encoded)
    
    tensor = torch.tensor([padded_seq])
    
    output = model(tensor)
    pred = torch.argmax(output, dim=1).item()
    
    reverse_map = {v:k for k,v in label_map.items()}
    return reverse_map[pred]


print("\nPredictions:")
print(predict("Zomato order 300"))  
print(predict("Uber trip 150"))      
print(predict("Salary credited"))    