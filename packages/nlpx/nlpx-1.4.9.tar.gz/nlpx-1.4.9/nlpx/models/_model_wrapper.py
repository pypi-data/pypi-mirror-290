import torch
import numpy as np
import pandas as pd
from torch import optim
from pathlib import Path
from typing import Union, List, Tuple
from sklearn.model_selection import train_test_split
from torch.nn import functional as F
from torch.utils.data import DataLoader, TensorDataset, Dataset

from nlpx.llm import TokenizeVec
from nlpx.dataset import TokenDataset, PaddingTokenCollator
from nlpx.text_token import PaddingTokenizer, Tokenizer, TokenEmbedding
from nlpx.training import Trainer, SimpleTrainer, ClassTrainer, SimpleClassTrainer, SplitClassTrainer, evaluate


class ModelWrapper:
	
	def __init__(self, model_path: Union[str, Path] = None,
	             device=torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')):
		self.device = device
		self.model = torch.load(model_path, map_location=device) if model_path else None
	
	def train(self, model, train_set: Dataset, collate_fn=None, max_iter=100,
	          optimizer=optim.AdamW, learning_rate=0.001, T_max: int = 0,
	          batch_size=32, num_workers=0,
	          pin_memory: bool = False, pin_memory_device: str = "",
	          persistent_workers: bool = False,
	          early_stopping_rounds: int = 10,
	          print_per_rounds: int = 1):
		trainer = Trainer(max_iter, optimizer, learning_rate, T_max,
		                  batch_size,
		                  num_workers,
		                  pin_memory, pin_memory_device,
		                  persistent_workers,
		                  early_stopping_rounds,  # 早停，等10轮决策，评价指标不在变化，停止
		                  print_per_rounds,
		                  self.device)
		self.model = trainer.train(model, train_set, collate_fn)
	
	def logits(self, X: torch.Tensor):
		self.model.eval()
		with torch.no_grad():
			logits = self.model(X)
		return logits
	
	def save(self, model_path: Union[str, Path] = './best_model.pt'):
		torch.save(self.model, model_path)
	
	def load(self, model_path: Union[str, Path] = './best_model.pt'):
		self.model = torch.load(model_path, map_location=self.device)


class SimpleModelWrapper(ModelWrapper):
	
	def __init__(self, model_path: Union[str, Path] = None,
	             device=torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')):
		super().__init__(model_path, device)
	
	def train(self, model, X: Union[torch.Tensor, np.ndarray, List], y: Union[torch.LongTensor, np.ndarray, List],
	          collate_fn=None, max_iter=100,
	          optimizer=optim.AdamW, learning_rate=0.001, T_max: int = 0,
	          batch_size=32, num_workers=0,
	          pin_memory: bool = False, pin_memory_device: str = "",
	          persistent_workers: bool = False,
	          early_stopping_rounds: int = 10,
	          print_per_rounds: int = 1):
		trainer = SimpleTrainer(max_iter, optimizer, learning_rate, T_max,
		                        batch_size,
		                        num_workers,
		                        pin_memory, pin_memory_device,
		                        persistent_workers,
		                        early_stopping_rounds,  # 早停，等10轮决策，评价指标不在变化，停止
		                        print_per_rounds,
		                        self.device)
		self.model = trainer.train(model, X, y, collate_fn)


class ClassModelWrapper(ModelWrapper):
	
	def __init__(self, model_path: Union[str, Path] = None, classes: List[str] = None,
	             device=torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')):
		self.classes = classes
		self.device = device
		self.model = torch.load(model_path, map_location=device) if model_path else None
	
	def train(self, model, train_set: Dataset, eval_set: Dataset, collate_fn=None, max_iter=100,
	          optimizer=optim.AdamW, learning_rate=0.001, T_max: int = 0,
	          batch_size=32, eval_batch_size=64,
	          num_workers=0, num_eval_workers=0,
	          pin_memory: bool = False, pin_memory_device: str = "",
	          persistent_workers: bool = False,
	          early_stopping_rounds: int = 10,
	          print_per_rounds: int = 1):
		trainer = ClassTrainer(max_iter, optimizer, learning_rate, T_max,
		                       batch_size, eval_batch_size,
		                       num_workers, num_eval_workers,
		                       pin_memory, pin_memory_device,
		                       persistent_workers,
		                       early_stopping_rounds,  # 早停，等10轮决策，评价指标不在变化，停止
		                       print_per_rounds,
		                       self.device)
		self.model = trainer.train(model, train_set, eval_set, collate_fn)
	
	def predict(self, X: torch.Tensor):
		logits = self.logits(X)
		return logits.argmax(1)
	
	def predict_classes(self, X: torch.Tensor):
		assert self.classes is not None, 'classes must be specified'
		pred = self.predict(X)
		return [self.classes[i] for i in pred.detach().numpy().ravel()]
	
	def predict_proba(self, X: torch.Tensor):
		logits = self.logits(X)
		result = F.softmax(logits, dim=1).max(1)
		return result.indices, result.values.numpy()
	
	def predict_classes_proba(self, X: torch.Tensor):
		assert self.classes is not None, 'classes must be specified'
		indices, values = self.predict_proba(X)
		return [self.classes[i] for i in indices.detach().numpy().ravel()], values
	
	def evaluate(self, eval_set: Dataset, batch_size=16, num_workers=0, max_length: int = None, collate_fn=None):
		eval_loader = DataLoader(dataset=eval_set, batch_size=batch_size,
		                         num_workers=num_workers, collate_fn=collate_fn)
		_, acc = evaluate(self.model, eval_loader, self.device)
		return acc


class SimpleClassModelWrapper(ClassModelWrapper):
	
	def __init__(self, model_path: Union[str, Path] = None, classes: List[str] = None,
	             device=torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')):
		super().__init__(model_path, classes, device)
	
	def train(self, model, X: Union[torch.Tensor, np.ndarray, List], y: Union[torch.LongTensor, np.ndarray, List],
	          eval_data: Tuple[Union[torch.Tensor, np.ndarray, List], Union[torch.LongTensor, np.ndarray, List]],
	          collate_fn=None, max_iter=100,
	          optimizer=optim.AdamW, learning_rate=0.001, T_max: int = 0,
	          batch_size=32, eval_batch_size=64,
	          num_workers=0, num_eval_workers=0,
	          pin_memory: bool = False, pin_memory_device: str = "",
	          persistent_workers: bool = False,
	          early_stopping_rounds: int = 10,
	          print_per_rounds: int = 1):
		trainer = SimpleClassTrainer(max_iter, optimizer, learning_rate, T_max,
		                             batch_size, eval_batch_size,
		                             num_workers, num_eval_workers,
		                             pin_memory, pin_memory_device,
		                             persistent_workers,
		                             early_stopping_rounds,
		                             print_per_rounds,
		                             self.device)
		self.model = trainer.train(model, X, y, eval_data, collate_fn)


class TextModelWrapper(ClassModelWrapper):
	
	def __init__(self, tokenize_vec: Union[PaddingTokenizer, Tokenizer, TokenizeVec, TokenEmbedding],
	             model_path: Union[str, Path] = None, classes: List[str] = None,
	             device=torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')):
		super().__init__(model_path, classes, device)
		self.tokenize_vec = tokenize_vec
	
	def train(self, model, texts: Union[List[str], np.ndarray, pd.Series], y: Union[torch.LongTensor, np.ndarray, List],
	          max_length: int = None, eval_size=0.2, random_state=None, collate_fn=None, max_iter=100,
	          optimizer=optim.AdamW, learning_rate=0.001, T_max: int = 0,
	          batch_size=32, eval_batch_size=64,
	          num_workers=0, num_eval_workers=0,
	          pin_memory: bool = False, pin_memory_device: str = "",
	          persistent_workers: bool = False,
	          early_stopping_rounds: int = 10,
	          print_per_rounds: int = 1, n_jobs=-1):
		X = self.get_vec(texts, max_length=max_length, n_jobs=n_jobs)
		trainer = SplitClassTrainer(max_iter, optimizer, learning_rate, T_max,
		                            batch_size, eval_batch_size,
		                            num_workers, num_eval_workers,
		                            pin_memory, pin_memory_device,
		                            persistent_workers,
		                            early_stopping_rounds,
		                            print_per_rounds,
		                            self.device)
		self.model = trainer.train(model, X, y, eval_size, random_state, collate_fn)
	
	def predict(self, texts: List[str], max_length: int = None, n_jobs=-1):
		logits = self.logits(texts, max_length, n_jobs=n_jobs)
		return logits.argmax(1)
	
	def predict_classes(self, texts: List[str], max_length: int = None, n_jobs=-1):
		assert self.classes is not None, 'classes must be specified'
		pred = self.predict(texts, max_length, n_jobs=n_jobs)
		return [self.classes[i] for i in pred.detach().numpy().ravel()]
	
	def predict_proba(self, texts: List[str], max_length: int = None, n_jobs=-1):
		logits = self.logits(texts, max_length, n_jobs=n_jobs)
		result = F.softmax(logits, dim=1).max(1)
		return result.indices, result.values.numpy()
	
	def predict_classes_proba(self, texts: List[str], max_length: int = None, n_jobs=-1):
		assert self.classes is not None, 'classes must be specified'
		indices, values = self.predict_proba(texts, max_length, n_jobs)
		return [self.classes[i] for i in indices.detach().numpy().ravel()], values
	
	def logits(self, texts: List[str], max_length: int = None, n_jobs=-1):
		X = self.get_vec(texts, max_length, n_jobs=n_jobs)
		return super().logits(X)
	
	def evaluate(self, texts: Union[str, List[str], np.ndarray, pd.Series],
	             y: Union[torch.LongTensor, np.ndarray, List], batch_size=16, num_workers=0,
	             max_length: int = None, collate_fn=None, n_jobs=-1):
		X = self.get_vec(texts, max_length, n_jobs=n_jobs)
		if isinstance(y, (np.ndarray, List)):
			y = torch.tensor(y, dtype=torch.long)
		eval_set = TensorDataset(X, y)
		return super().evaluate(eval_set, batch_size=batch_size, num_workers=num_workers, collate_fn=collate_fn)
	
	def get_vec(self, texts: Union[str, List[str], np.ndarray, pd.Series], max_length: int, n_jobs: int):
		if isinstance(texts, str):
			texts = [texts]
		
		if isinstance(self.tokenize_vec, TokenizeVec):
			return self.tokenize_vec.parallel_encode_plus(texts, max_length=max_length, padding='max_length',
			                                              truncation=True, add_special_tokens=True,
			                                              return_token_type_ids=True, return_attention_mask=True,
			                                              return_tensors='pt', n_jobs=n_jobs)
		
		elif isinstance(self.tokenize_vec, (PaddingTokenizer, Tokenizer)):
			return torch.LongTensor(self.tokenize_vec.batch_encode(texts, max_length))
		
		elif isinstance(self.tokenize_vec, TokenEmbedding):
			return self.tokenize_vec(texts, max_length)
		
		raise ValueError("Invalid tokenize_vec, it must be a TokenizeVec or TokenEmbedding.")
	
	
class PaddingTextModelWrapper(ClassModelWrapper):
	
	def __init__(self, tokenizer: Union[PaddingTokenizer, Tokenizer], model_path: Union[str, Path] = None,
	             classes: List[str] = None, device=torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')):
		super().__init__(model_path, classes, device)
		self.tokenizer = tokenizer
		
	def train(self, model, texts: Union[List[str], np.ndarray, pd.Series], y: Union[torch.LongTensor, np.ndarray, List],
	          max_length: int = None, eval_size=0.2, random_state=None, max_iter=100,
	          optimizer=optim.AdamW, learning_rate=0.001, T_max: int = 0,
	          batch_size=32, eval_batch_size=64,
	          num_workers=0, num_eval_workers=0,
	          pin_memory: bool = False, pin_memory_device: str = "",
	          persistent_workers: bool = False,
	          early_stopping_rounds: int = 10,
	          print_per_rounds: int = 1):
		X = self.tokenizer.batch_encode(texts, padding=False)
		X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=eval_size, random_state=random_state)
		train_set = TokenDataset(X_train, y_train)
		eval_set = TokenDataset(X_test, y_test)
		super().train(model, train_set, eval_set, PaddingTokenCollator(self.tokenizer.padding, max_length), max_iter, optimizer,
		              learning_rate, T_max, batch_size, eval_batch_size, num_workers, num_eval_workers, pin_memory,
		              pin_memory_device, persistent_workers, early_stopping_rounds, print_per_rounds)
	
	def predict(self, texts: List[str], max_length: int = None):
		logits = self.logits(texts, max_length)
		return logits.argmax(1)
	
	def predict_classes(self, texts: List[str], max_length: int = None):
		assert self.classes is not None, 'classes must be specified'
		pred = self.predict(texts, max_length)
		return [self.classes[i] for i in pred.detach().numpy().ravel()]
	
	def predict_proba(self, texts: List[str], max_length: int = None):
		logits = self.logits(texts, max_length)
		result = F.softmax(logits, dim=1).max(1)
		return result.indices, result.values.numpy()
	
	def predict_classes_proba(self, texts: List[str], max_length: int = None):
		assert self.classes is not None, 'classes must be specified'
		indices, values = self.predict_proba(texts, max_length)
		return [self.classes[i] for i in indices.detach().numpy().ravel()], values
	
	def logits(self, texts: List[str], max_length: int = None):
		X = self.tokenizer.batch_encode(texts, max_length)
		X = torch.tensor(X, dtype=torch.long)
		return super().logits(X)
	
	def evaluate(self, texts: Union[str, List[str], np.ndarray, pd.Series],
	             y: Union[torch.LongTensor, np.ndarray, List], batch_size=16, num_workers=0,
	             max_length: int = None):
		X = self.tokenizer.batch_encode(texts, padding=False)
		if isinstance(y, (np.ndarray, List)):
			y = torch.tensor(y, dtype=torch.long)
		eval_set = TokenDataset(X, y)
		return super().evaluate(eval_set, batch_size=batch_size, num_workers=num_workers,
		                        collate_fn=PaddingTokenCollator(self.tokenizer.padding, max_length))
	