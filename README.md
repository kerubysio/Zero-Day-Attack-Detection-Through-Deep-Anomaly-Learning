Here is a README drafted in English, keeping the tone natural, professional, and slightly conversational—perfect for a student showcasing their work on GitHub.

---

# Zero-Day Attack Detection Through Deep Anomaly Learning

Welcome to my repository! This project focuses on designing and implementing a Deep Learning-based Anomaly Detection system to identify Zero-Day network attacks.

Traditional Network Intrusion Detection Systems (NIDS) usually rely on comparing incoming traffic against a database of known malicious signatures. The obvious flaw here is that they are completely blind to zero-day threats—attacks exploiting undocumented vulnerabilities that don't have a signature yet.

To solve this, I flipped the approach: instead of teaching the model what an attack looks like, the system is trained exclusively on "benign" network traffic to learn normal behavior. Any traffic flow that significantly deviates from this learned normality is isolated and flagged as a potential threat.

## The Data & The Challenges

The model was trained and evaluated on the **UNSW-NB15** dataset, which contains over 2.5 million records. It includes normal traffic alongside various attack categories like exploits, worms, and shellcode, making it a great playground for simulating zero-day scenarios.

Working with this dataset presented two massive structural challenges:

* 
**Class Imbalance:** The volume of benign traffic absolutely dwarfs the individual attack categories.


* 
**Class Overlap:** Different types of attacks blend and overlap almost perfectly with normal traffic in the multidimensional feature space. This makes it incredibly hard to draw clear decision boundaries without exploding the false alarm rate.



## Data Preprocessing Pipeline

Raw network data is noisy and heavily skewed. To ensure the neural network could learn effectively, I built a robust preprocessing pipeline:

* 
**Categorical Encoding:** Text-based features like protocols (`proto`), services (`service`), and connection states (`state`) were converted into numerical tensors using One-Hot Encoding.


* 
**Outlier Management:** Network traffic has heavy-tailed distributions (e.g., transferred bytes ranging from a few digits to gigabytes). I applied a logarithmic compression (`numpy.log1p`) to dampen outliers while preserving variance on smaller values.


* 
**Scaling:** After the log transformation, the data was forced into a [0,1] range using a `MinMaxScaler`. Crucially, this scaler was fitted *only* on the benign traffic to respect the semi-supervised paradigm.



## Model Architecture

The core of the detection engine is a semi-supervised **Autoencoder** built with PyTorch.

* 
**The Encoder:** Uses `Linear` layers, `ReLU` activations, `BatchNorm1d`, and a 20% `Dropout` to progressively compress the input data down to a restricted 32-dimensional bottleneck. This forces the network to discard noise and memorize only the latent patterns of benign traffic.


* 
**The Decoder:** A mirrored module that takes this compressed vector and attempts to reconstruct the original features.


* 
**Detection Logic:** During inference, the model calculates the Mean Squared Error (MSE) between the real input and its reconstruction. If the MSE exceeds a dynamic threshold (set at the 99th percentile of the training errors), the packet is flagged as a Zero-Day attack.



## Results & KPIs

The system was engineered to meet strict Key Performance Indicators (KPIs). Here is how the optimized model performed on the test set:

| Metric | Achieved Value | Project KPI Target |
| --- | --- | --- |
| **Area Under the Curve (AUC)** | 0.9445 

 | > 0.90 

 |
| **False Alarm Rate (FAR)** | 4.31% 

 | < 5% 

 |
| **Detection Rate (DR)** | 74.23% 

 | > 95% 

 |

*Note on the Detection Rate:* While the AUC and FAR successfully hit the targets, the DR fell short of the 95% goal. Mathematical analysis of the ROC curve revealed that due to the severe class overlap in the UNSW-NB15 dataset, hitting a 95% DR while keeping false alarms under 5% requires a theoretical AUC of at least 0.95.

## Future Developments

This project serves as a solid baseline, but there is room for growth. Future iterations might explore:

* 
**Federated Learning:** To train models locally on distributed nodes (like corporate networks or IoT devices) without exposing raw, sensitive traffic data to a central server.


* 
**Online Learning:** Implementing continual learning mechanisms to periodically update the model with new benign examples, helping it adapt to evolving network behaviors (concept drift).


* 
**Quantum Machine Learning:** Exploring Quantum Autoencoders to map the latent space into an exponentially larger number of states using qubits, potentially improving the separation of overlapping classes.
