# 🛣️ ADVANCED IMPLEMENTATION ROADMAP

Panduan untuk mengimplementasi Stage 2 (CNN) dan Stage 3 (LSTM).

---

## 📊 Model Comparison

| Aspek | Random Forest | CNN | LSTM |
|-------|---------------|-----|------|
| Input | Landmarks (63) | Images (224×224×3) | Sequences of frames |
| Training Time | ⚡ 1-5 min | 💻 10-60 min | ⏳ 30+ min |
| Inference | ⚡ 1ms | 💻 5-10ms | ⏳ 20-50ms |
| Accuracy | 90-96% | 95-99% | 95-99%+ |
| GPU Required | ❌ No | ⚠️ Recommended | ✅ Yes |
| Best For | Static letters | Better generalization | Sequences/words |
| Code Complexity | ⭐ Simple | ⭐⭐ Medium | ⭐⭐⭐ Complex |

---

## 🚀 Phase 4 Stage 2: CNN + Transfer Learning

### Architecture

```
Input: Image (224×224×3)
   ↓
[MobileNetV2 - Pre-trained on ImageNet]
   - Frozen layers (feature extraction)
   ↓
[Global Average Pooling]
   ↓
[Dense(512) + ReLU]
[Dropout(0.3)]
   ↓
[Dense(26) + Softmax]  ← Output (26 classes)
```

### Implementation Plan

**File:** `src/phase4_model_training/stage2_cnn_transfer_learning.py`

```python
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

def build_cnn_model(num_classes=26):
    \"\"\"Build CNN with transfer learning.\"\"\"
    
    # Load pre-trained MobileNetV2
    base_model = MobileNetV2(
        input_shape=(224, 224, 3),
        include_top=False,
        weights='imagenet'
    )
    
    # Freeze base model
    base_model.trainable = False
    
    # Build custom head
    model = models.Sequential([
        layers.Input(shape=(224, 224, 3)),
        layers.Lambda(lambda x: preprocess_input(x)),
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dense(512, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    return model

# Training
model = build_cnn_model(num_classes=26)
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# Fit dengan ImageDataLoader
history = model.fit(
    X_train, y_train,
    epochs=20,
    batch_size=32,
    validation_split=0.2,
    callbacks=[
        tf.keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=3,
            restore_best_weights=True
        )
    ]
)
```

### Key Points

- Use MobileNetV2 untuk speed (lebih cepat dari ResNet)
- Freeze base model (jangan retrain ImageNet weights)
- Data augmentation sangat penting untuk CNN
- Gunakan GPU untuk training (jauh lebih cepat)

### Expected Results

- Accuracy: 95-99%
- Training time: 10-60 minutes (GPU)
- Model size: 30-50 MB

---

## 🚀 Phase 4 Stage 3: LSTM for Sequences

### Architecture

```
Input: Sequence of frames [T, 224, 224, 3]
   ↓
[TimeDistributed(CNN features)] ← MobileNetV2 features
   ↓
[LSTM(256, return_sequences=True)]
[Dropout(0.2)]
   ↓
[LSTM(128, return_sequences=False)]
[Dropout(0.2)]
   ↓
[Dense(26) + Softmax]
```

### Implementation Plan

**File:** `src/phase4_model_training/stage3_lstm_sequence.py`

```python
from tensorflow.keras.applications import MobileNetV2

def build_lstm_model(seq_length=10, num_classes=26):
    \"\"\"Build LSTM model for sequence recognition.\"\"\"
    
    # Feature extractor (pre-trained CNN)
    base_model = MobileNetV2(
        input_shape=(224, 224, 3),
        include_top=False,
        weights='imagenet'
    )
    base_model.trainable = False
    
    model = models.Sequential([
        layers.Input(shape=(seq_length, 224, 224, 3)),
        layers.TimeDistributed(base_model),
        layers.TimeDistributed(layers.GlobalAveragePooling2D()),
        layers.LSTM(256, return_sequences=True, activation='relu'),
        layers.Dropout(0.2),
        layers.LSTM(128, return_sequences=False, activation='relu'),
        layers.Dropout(0.2),
        layers.Dense(64, activation='relu'),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    return model

# Prepare sequence data
def prepare_sequences(video_path, seq_length=10):
    \"\"\"Extract sequence of frames from video.\"\"\"
    cap = cv2.VideoCapture(video_path)
    frames = []
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, (224, 224))
        frames.append(frame)
    
    cap.release()
    
    # Reshape to sequences
    sequences = []
    for i in range(len(frames) - seq_length):
        sequences.append(frames[i:i+seq_length])
    
    return np.array(sequences)
```

### Key Points

- Use pre-extracted CNN features untuk speed
- LSTM belajar temporal dependencies
- Require video/sequence data (bukan static images)
- Memory intensive (gunakan GPU)

### Expected Results

- Accuracy: 95-99%+
- Training time: 30+ minutes (GPU)
- Model size: 50-100 MB

---

## 📋 Implementation Checklist

### Stage 2: CNN
- [ ] Create `stage2_cnn_transfer_learning.py`
- [ ] Build MobileNetV2 model
- [ ] Implement ImageDataLoader
- [ ] Add data augmentation
- [ ] Train model with callbacks
- [ ] Evaluate & compare with Random Forest
- [ ] Save model & weights
- [ ] Test with real-time integration

### Stage 3: LSTM
- [ ] Create `stage3_lstm_sequence.py`
- [ ] Prepare video/sequence data
- [ ] Build LSTM model with TimeDistributed
- [ ] Create sequence generator
- [ ] Train model
- [ ] Evaluate performance
- [ ] Save model
- [ ] Update real-time prediction (for sequences)

---

## 🔧 Data Preparation for CNN

```python
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Augmentation pipeline
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

test_datagen = ImageDataGenerator(rescale=1./255)

# Load images
train_generator = train_datagen.flow_from_directory(
    'dataset/sibi',
    target_size=(224, 224),
    batch_size=32,
    class_mode='sparse'
)

validation_generator = test_datagen.flow_from_directory(
    'dataset/sibi',
    target_size=(224, 224),
    batch_size=32,
    class_mode='sparse'
)
```

---

## 💾 Model Optimization Techniques

### 1. **Quantization** (Reduce model size)
```python
import tensorflow as tf

converter = tf.lite.TFLiteConverter.from_saved_model("saved_model/")
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_model = converter.convert()

with open("model_quantized.tflite", "wb") as f:
    f.write(tflite_model)
```

### 2. **Pruning** (Remove unnecessary weights)
```python
import tensorflow_model_optimization as tfmot

pruning_schedule = tfmot.sparsity.keras.PolynomialDecay(
    initial_sparsity=0.36,
    final_sparsity=0.8,
    begin_step=0,
    end_step=len(train_data)*epochs
)

pruned_model = tfmot.sparsity.keras.prune_low_magnitude(
    model,
    pruning_schedule=pruning_schedule
)
```

### 3. **Distillation** (Smaller but still accurate)
```python
# Train smaller model from larger teacher model
student = build_small_cnn(num_classes=26)
teacher = load_trained_cnn()

# Use teacher predictions as soft targets
distillation_loss = tf.keras.losses.KLDivergence()
```

---

## 🚀 Deployment Considerations

### Edge Devices (Raspberry Pi, Android)
1. Use TensorFlow Lite
2. Quantize model (int8)
3. Reduce input resolution (160×160)
4. Use lightweight architecture

### Cloud Deployment
1. Use full model (better accuracy)
2. Batch processing possible
3. GPU acceleration
4. REST API for requests

### Real-time Desktop App
1. Use optimized model
2. Cache predictions
3. Multi-threading for camera
4. Minimal preprocessing

---

## 📚 Recommended Learning Resources

### TensorFlow/Keras
- [TensorFlow official tutorials](https://www.tensorflow.org/tutorials)
- [Keras documentation](https://keras.io/)
- [Transfer learning guide](https://www.tensorflow.org/guide/transfer_learning)

### Computer Vision
- [MobileNet paper](https://arxiv.org/abs/1704.04861)
- [ImageNet dataset](http://www.image-net.org/)
- [OpenCV tutorials](https://docs.opencv.org/master/d9/df8/tutorial_root.html)

### Deep Learning
- [LSTM tutorial](http://colah.github.io/posts/2015-08-Understanding-LSTMs/)
- [Sequence modeling](https://karpathy.github.io/2015/05/21/rnn-effectiveness/)

---

## ⚙️ Hyperparameter Tuning

### CNN Hyperparameters
```python
# Learning rate schedule
lr_schedule = tf.keras.optimizers.schedules.ExponentialDecay(
    initial_learning_rate=0.001,
    decay_steps=1000,
    decay_rate=0.96,
    staircase=True
)

optimizer = tf.keras.optimizers.Adam(learning_rate=lr_schedule)

# Batch size trade-off
# - Larger batch (64, 128): Better gradient, faster, needs more memory
# - Smaller batch (16, 32): Slower, less memory, noisier gradient
```

### LSTM Hyperparameters
```python
# Sequence length
seq_length = 10  # 10 frames
# Impact: Longer = more memory but captures more context

# Hidden units
lstm_units = 256  # First layer
# Impact: More units = more capacity but more parameters

# Dropout rate
dropout_rate = 0.2  # 20% dropout
# Impact: Higher = more regularization but slower training
```

---

## 🔍 Evaluation Metrics

### Classification Metrics
```python
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, 
    f1_score, confusion_matrix, roc_auc_score
)

# For multi-class
precision = precision_score(y_true, y_pred, average='weighted')
recall = recall_score(y_true, y_pred, average='weighted')
f1 = f1_score(y_true, y_pred, average='weighted')
```

### Per-Class Analysis
```python
from sklearn.metrics import classification_report

report = classification_report(
    y_true, y_pred,
    target_names=class_names,
    output_dict=True
)

# Find hard-to-classify letters
for letter, metrics in report.items():
    if metrics['f1-score'] < 0.9:
        print(f"⚠️ {letter} has low F1-score: {metrics['f1-score']}")
```

---

## 📈 Training Pipeline

```python
# Complete training pipeline
def train_cnn(X_train, y_train, X_val, y_val):
    model = build_cnn_model()
    
    callbacks = [
        EarlyStopping(monitor='val_loss', patience=5),
        ReduceLROnPlateau(factor=0.5, patience=3),
        ModelCheckpoint('best_model.h5', save_best_only=True),
        TensorBoard(log_dir='logs/')
    ]
    
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=100,
        batch_size=32,
        callbacks=callbacks
    )
    
    return model, history
```

---

## ✅ Testing Checklist

- [ ] Model trained successfully
- [ ] Accuracy > 90% on test set
- [ ] Per-class performance balanced
- [ ] No overfitting (train ≈ test accuracy)
- [ ] Inference speed acceptable (<100ms)
- [ ] Model exports correctly
- [ ] Real-time inference works
- [ ] Compare with previous stage

---

## 🎯 Performance Targets

### Stage 2: CNN
- Overall accuracy: ≥95%
- Per-letter F1-score: ≥0.90
- Inference latency: <50ms
- Model size: <50MB

### Stage 3: LSTM
- Overall accuracy: ≥97%
- Per-letter F1-score: ≥0.95
- Sequence latency: <100ms
- Model size: <100MB

---

## 🚀 Next: Implementation

When ready, implement:
1. Copy this roadmap
2. Create `src/phase4_model_training/stage2_cnn_transfer_learning.py`
3. Follow the architecture & code samples
4. Train & evaluate
5. Update `realtime_prediction.py` to support CNN
6. Repeat for Stage 3 (LSTM)

---

**Ready to implement? Start coding! 🚀**
