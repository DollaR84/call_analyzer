import logging
import time
from typing import Any, Optional

import numpy as np
from speechbrain.inference.speaker import SpeakerRecognition
from sklearn.cluster import AgglomerativeClustering
from tqdm import tqdm
import torch
import torchaudio

from core.types import Device
from schemas import TranscriptSegment


logger = logging.getLogger(__name__)


class DiarizationClient:

    def __init__(self, device: Device):
        start_time = time.time()

        with tqdm(total=0, bar_format="{desc}", desc="Loading diarization model into memory... "):
            self.encoder = SpeakerRecognition.from_hparams(
                source="speechbrain/spkrec-ecapa-voxceleb",
                run_opts={"device": device}
            )

        logger.info("diarization model loaded successfully in %.2f seconds!", time.time() - start_time)

    def diarization(
            self,
            audio_path: str,
            segments: list[TranscriptSegment],
            num_speakers: Optional[int] = 2,
    ) -> list[TranscriptSegment]:
        signal, fs = torchaudio.load(audio_path)

        if signal.shape[0] > 1:
            signal = torch.mean(signal, dim=0, keepdim=True)

        if fs != 16000:
            resampler = torchaudio.transforms.Resample(orig_freq=fs, new_freq=16000)
            signal = resampler(signal)
            fs = 16000

        train_embeddings = []
        train_segments_idx = []
        all_embeddings: list[Optional[np.ndarray]] = []

        for idx, segment in enumerate(segments):
            start_sample = int(segment.start * fs)
            end_sample = int(segment.end * fs)
            segment_signal = signal[:, start_sample:end_sample]

            if segment_signal.shape[1] == 0:
                all_embeddings.append(None)
                continue

            with torch.no_grad():
                embedding = self.encoder.encode_batch(segment_signal)
                emb_np = embedding.cpu().numpy().flatten()

                norm = np.linalg.norm(emb_np)
                if norm > 0:
                    emb_np = emb_np / norm

                all_embeddings.append(emb_np)

                if segment_signal.shape[1] >= int(1.0 * fs):
                    train_embeddings.append(emb_np)
                    train_segments_idx.append(idx)

        if len(train_embeddings) < (num_speakers or 2):
            train_embeddings = []
            train_segments_idx = []
            for idx, segment in enumerate(segments):
                start_sample = int(segment.start * fs)
                end_sample = int(segment.end * fs)
                segment_signal = signal[:, start_sample:end_sample]

                if segment_signal.shape[1] >= int(0.5 * fs) and all_embeddings[idx] is not None:
                    train_embeddings.append(all_embeddings[idx])
                    train_segments_idx.append(idx)

        if len(train_embeddings) <= 1:
            logger.warning("Not enough valid segments to split votes.")
            return segments

        np_train_embeddings = np.array(train_embeddings)
        mean_emb = np.mean(np_train_embeddings, axis=0)
        np_train_embeddings = np_train_embeddings - mean_emb
        norms = np.linalg.norm(np_train_embeddings, axis=1, keepdims=True)
        np_train_embeddings = np.where(norms > 0, np_train_embeddings / norms, np_train_embeddings)

        kwargs: dict[str, Any] = {
            "metric": "cosine",
            "linkage": "complete",
        }

        if num_speakers and len(np_train_embeddings) >= num_speakers:
            kwargs["n_clusters"] = num_speakers
        else:
            kwargs["n_clusters"] = None
            kwargs["distance_threshold"] = 0.7

        clusterer = AgglomerativeClustering(**kwargs)
        train_labels = clusterer.fit_predict(np_train_embeddings)

        for idx, segment in enumerate(segments):
            if all_embeddings[idx] is None:
                segment.speaker = segments[idx - 1].speaker if idx > 0 else "Speaker_0"
                continue

            if idx in train_segments_idx:
                label_idx = train_segments_idx.index(idx)
                segment.speaker = f"Speaker_{train_labels[label_idx]}"
            else:
                current_emb = all_embeddings[idx] - mean_emb
                norm = np.linalg.norm(current_emb)
                if norm > 0:
                    current_emb /= norm

                cos_distances = 1.0 - np.dot(np_train_embeddings, current_emb)
                closest_train_idx = np.argmin(cos_distances)
                segment.speaker = f"Speaker_{train_labels[closest_train_idx]}"

        return segments
