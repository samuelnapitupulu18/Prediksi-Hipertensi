"""
Social Group Optimization (SGO)
===============================

Implementasi algoritma Social Group Optimization sesuai rumusan asli:

    Satapathy, S. & Naik, A. (2016). "Social group optimization (SGO):
    a new population evolutionary optimization technique."
    Complex & Intelligent Systems, 2(3), 173-203.

SGO meniru cara sekelompok orang memecahkan masalah lewat dua fase pada setiap
generasi:

1. IMPROVING PHASE — setiap orang memperbaiki diri dengan belajar dari orang
   terbaik dalam kelompok (gbest):

       X_baru[i][j] = c * X_lama[i][j] + r * (gbest[j] - X_lama[i][j])

   c adalah faktor introspeksi diri (self-introspection), r bilangan acak [0,1].

2. ACQUIRING PHASE — setiap orang bertukar pengetahuan dengan satu orang lain
   yang dipilih acak (X_r), sekaligus tetap belajar dari gbest:

       bila f(X_i) lebih baik dari f(X_r):
           X_baru[i][j] = X_i[j] + r1*(X_i[j] - X_r[j]) + r2*(gbest[j] - X_i[j])
       bila sebaliknya:
           X_baru[i][j] = X_i[j] + r1*(X_r[j] - X_i[j]) + r2*(gbest[j] - X_i[j])

Pada kedua fase dipakai greedy selection: posisi baru hanya diterima bila nilai
fitness-nya lebih baik daripada posisi lama.

Modul ini sengaja dibuat tidak bergantung pada XGBoost — ia hanya menerima
sebuah fungsi fitness, sehingga bisa diuji terpisah.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Sequence, Tuple

import numpy as np


@dataclass
class SearchSpace:
    """Batas pencarian satu hyperparameter."""

    name: str
    low: float
    high: float
    is_integer: bool = False

    def clip(self, value: float) -> float:
        value = float(np.clip(value, self.low, self.high))
        return float(round(value)) if self.is_integer else value


@dataclass
class IterationRecord:
    """Catatan satu iterasi, dipakai untuk grafik konvergensi di frontend."""

    iteration: int
    best_fitness: float
    mean_fitness: float
    best_params: Dict[str, float]
    elapsed_s: float


@dataclass
class SGOResult:
    best_params: Dict[str, float]
    best_fitness: float
    history: List[IterationRecord] = field(default_factory=list)
    n_evaluations: int = 0
    elapsed_s: float = 0.0


class SocialGroupOptimizer:
    """
    Optimizer SGO untuk memaksimalkan sebuah fungsi fitness.

    Parameters
    ----------
    space:
        Daftar SearchSpace — satu per hyperparameter yang dicari.
    fitness_fn:
        Fungsi yang menerima dict hyperparameter dan mengembalikan skor
        (semakin besar semakin baik).
    population_size:
        Jumlah "orang" dalam kelompok.
    iterations:
        Jumlah generasi. Inilah nilai yang diatur manual oleh pengguna.
    c:
        Faktor introspeksi diri pada improving phase (default 0.2 sesuai paper).
    seed:
        Seed acak agar hasil dapat direproduksi.
    """

    def __init__(
        self,
        space: Sequence[SearchSpace],
        fitness_fn: Callable[[Dict[str, float]], float],
        population_size: int = 6,
        iterations: int = 10,
        c: float = 0.2,
        seed: int = 42,
    ) -> None:
        if population_size < 3:
            raise ValueError("population_size minimal 3 agar acquiring phase bermakna.")
        if iterations < 1:
            raise ValueError("iterations minimal 1.")

        self.space = list(space)
        self.fitness_fn = fitness_fn
        self.population_size = population_size
        self.iterations = iterations
        self.c = c
        self.rng = np.random.default_rng(seed)
        self._n_eval = 0

    # ------------------------------------------------------------------ utils
    def _to_params(self, vector: np.ndarray) -> Dict[str, float]:
        return {s.name: s.clip(vector[j]) for j, s in enumerate(self.space)}

    def _evaluate(self, vector: np.ndarray) -> float:
        self._n_eval += 1
        return self.fitness_fn(self._to_params(vector))

    def _clip_vector(self, vector: np.ndarray) -> np.ndarray:
        return np.array([s.clip(vector[j]) for j, s in enumerate(self.space)], dtype=float)

    def _init_population(self) -> np.ndarray:
        lows = np.array([s.low for s in self.space], dtype=float)
        highs = np.array([s.high for s in self.space], dtype=float)
        pop = self.rng.uniform(lows, highs, size=(self.population_size, len(self.space)))
        return np.array([self._clip_vector(row) for row in pop])

    # ------------------------------------------------------------------- main
    def optimize(self, on_iteration: Callable[[IterationRecord], None] | None = None) -> SGOResult:
        started = time.perf_counter()

        population = self._init_population()
        fitness = np.array([self._evaluate(ind) for ind in population], dtype=float)

        best_idx = int(np.argmax(fitness))
        gbest = population[best_idx].copy()
        gbest_fitness = float(fitness[best_idx])

        history: List[IterationRecord] = []

        for it in range(1, self.iterations + 1):
            iter_started = time.perf_counter()

            # ---------------------------------------------------- fase 1
            # IMPROVING PHASE — semua orang belajar dari yang terbaik
            for i in range(self.population_size):
                r = self.rng.random(len(self.space))
                candidate = self.c * population[i] + r * (gbest - population[i])
                candidate = self._clip_vector(candidate)

                cand_fitness = self._evaluate(candidate)
                if cand_fitness > fitness[i]:          # greedy selection
                    population[i] = candidate
                    fitness[i] = cand_fitness

            best_idx = int(np.argmax(fitness))
            if fitness[best_idx] > gbest_fitness:
                gbest = population[best_idx].copy()
                gbest_fitness = float(fitness[best_idx])

            # ---------------------------------------------------- fase 2
            # ACQUIRING PHASE — bertukar pengetahuan dengan orang lain
            for i in range(self.population_size):
                r_idx = int(self.rng.integers(self.population_size))
                while r_idx == i:
                    r_idx = int(self.rng.integers(self.population_size))

                r1 = self.rng.random(len(self.space))
                r2 = self.rng.random(len(self.space))

                if fitness[i] > fitness[r_idx]:
                    direction = population[i] - population[r_idx]
                else:
                    direction = population[r_idx] - population[i]

                candidate = population[i] + r1 * direction + r2 * (gbest - population[i])
                candidate = self._clip_vector(candidate)

                cand_fitness = self._evaluate(candidate)
                if cand_fitness > fitness[i]:          # greedy selection
                    population[i] = candidate
                    fitness[i] = cand_fitness

            best_idx = int(np.argmax(fitness))
            if fitness[best_idx] > gbest_fitness:
                gbest = population[best_idx].copy()
                gbest_fitness = float(fitness[best_idx])

            record = IterationRecord(
                iteration=it,
                best_fitness=round(gbest_fitness, 6),
                mean_fitness=round(float(np.mean(fitness)), 6),
                best_params=self._to_params(gbest),
                elapsed_s=round(time.perf_counter() - iter_started, 3),
            )
            history.append(record)
            if on_iteration is not None:
                on_iteration(record)

        return SGOResult(
            best_params=self._to_params(gbest),
            best_fitness=round(gbest_fitness, 6),
            history=history,
            n_evaluations=self._n_eval,
            elapsed_s=round(time.perf_counter() - started, 3),
        )
