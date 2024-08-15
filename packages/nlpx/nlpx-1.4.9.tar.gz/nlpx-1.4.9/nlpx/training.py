import numpy as np
from typing import List, Tuple
import torch
from torch import optim
from torch.utils.data import DataLoader, TensorDataset, Dataset
from torch.optim.lr_scheduler import CosineAnnealingLR
from sklearn.model_selection import train_test_split
from nlpx import log_utils

E = 1e-5
E_CLASS = 1e-8


def evaluate(model, eval_loader, device):
	total = 0.0
	losses = 0.0
	correct = 0.0
	model.eval()
	with torch.no_grad():
		for batch in eval_loader:
			batch = [x.to(device) for x in batch]
			# batch = [x.to(device) if torch.is_tensor(x) else x for x in batch]
			y = batch[1]
			logits, loss = model(*batch)
			correct += (logits.argmax(1) == y).sum().item()
			losses += loss.item()
			total += len(y)
	return losses / total, correct / total


class Trainer:
	
	def __init__(self, max_iter=100, optimizer=optim.AdamW, learning_rate=0.001, T_max: int = 0, batch_size=32,
	             num_workers=0,
	             pin_memory: bool = False, pin_memory_device: str = "", persistent_workers: bool = False,
	             early_stopping_rounds: int = 2,  # 早停，等10轮决策，评价指标不在变化，停止
	             print_per_rounds: int = 1,
	             device=torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
	             ):
		self.max_iter = max_iter
		self.optimizer = optimizer
		self.learning_rate = learning_rate
		self.T_max = T_max
		self.batch_size = batch_size
		self.num_workers = num_workers
		self.pin_memory = pin_memory
		self.pin_memory_device = pin_memory_device
		self.persistent_workers = persistent_workers
		self.early_stopping_rounds = early_stopping_rounds
		self.print_per_rounds = print_per_rounds
		self.device = device
	
	def train(self, model, train_set: Dataset, collate_fn=None):
		train_loader = DataLoader(dataset=train_set, batch_size=self.batch_size, pin_memory=self.pin_memory,
		                          pin_memory_device=self.pin_memory_device, persistent_workers=self.persistent_workers,
		                          num_workers=self.num_workers, shuffle=True, collate_fn=collate_fn)
		if self.T_max and self.T_max > 0:
			scheduler = CosineAnnealingLR(self.optimizer, T_max=self.T_max)
			return self._train_scheduler(model.to(self.device), train_loader, scheduler)
		else:
			return self._train(model.to(self.device), train_loader)
	
	def _train(self, model, train_loader: DataLoader):
		cnt = 0
		min_loss = 1000000.0
		best_model = None
		optimizer = self.optimizer(model.parameters(), lr=self.learning_rate)
		model.train()
		for epoch in range(self.max_iter):
			total = 0.0
			losses = 0.0
			for batch in train_loader:
				batch = [x.to(self.device) for x in batch]
				y = batch[1]
				logits, loss = model(*batch)
				optimizer.zero_grad()
				loss.backward()
				optimizer.step()
				
				losses += loss.item()
				total += len(y)
			
			avg_loss = losses / total
			if self.print_per_rounds == 1:
				self.print(epoch, optimizer.param_groups[0]["lr"], avg_loss)
			elif self.print_per_rounds > 1:
				if epoch % self.print_per_rounds == 0:
					self.print(epoch, optimizer.param_groups[0]["lr"], avg_loss)
			
			if min_loss - avg_loss > E:
				best_model = model
				cnt = 0
				min_loss = avg_loss
				continue
			
			# x次epoch的val_acc不提升或x次epoch的val_acc不变化
			if epoch >= min(5, self.early_stopping_rounds) and cnt >= self.early_stopping_rounds:
				log_utils.info(f"Early stopping at epoch-{epoch}/{self.max_iter}")
				break
			
			cnt += 1
		
		return best_model
	
	def _train_scheduler(self, model, train_loader: DataLoader, scheduler: CosineAnnealingLR):
		cnt = 0
		min_loss = 1000000.0
		best_model = None
		optimizer = self.optimizer(model.parameters(), lr=self.learning_rate)
		model.train()
		for epoch in range(self.max_iter):
			total = 0.0
			losses = 0.0
			for batch in train_loader:
				batch = [x.to(self.device) for x in batch]
				y = batch[1]
				logits, loss = model(*batch)
				optimizer.zero_grad()
				loss.backward()
				optimizer.step()
				scheduler.step()
				
				losses += loss.item()
				total += len(y)
			
			avg_loss = losses / total
			if self.print_per_rounds == 1:
				self.print(epoch, optimizer.param_groups[0]["lr"], avg_loss)
			elif self.print_per_rounds > 1:
				if epoch % self.print_per_rounds == 0:
					self.print(epoch, optimizer.param_groups[0]["lr"], avg_loss)
			
			if min_loss - avg_loss > E:
				best_model = model
				cnt = 0
				min_loss = avg_loss
				continue
			
			# x次epoch的val_acc不提升或x次epoch的val_acc不变化
			if epoch >= min(3, self.early_stopping_rounds) and cnt >= self.early_stopping_rounds:
				log_utils.info(f"Early stopping at epoch-{epoch}/{self.max_iter}")
				break
			
			cnt += 1
		
		return best_model
	
	def print(self, epoch, lr, loss):
		log_utils.info(f'epoch-{epoch}/{self.max_iter}  lr: {lr:.6f}, loss: {loss:.6f}')


class SimpleTrainer(Trainer):
	
	def __init__(self, max_iter=100, optimizer=optim.AdamW, learning_rate=0.001, T_max: int = 0,
	             batch_size=32, num_workers=1,
	             pin_memory: bool = False, pin_memory_device: str = "",
	             persistent_workers: bool = False,
	             early_stopping_rounds=10,  # 早停，等10轮决策，评价指标不在变化，停止
	             print_per_rounds: int = 1,
	             device=torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')):
		super().__init__(max_iter,
		                 optimizer,
		                 learning_rate,
		                 T_max,
		                 batch_size,
		                 num_workers,
		                 pin_memory,
		                 pin_memory_device,
		                 persistent_workers,
		                 early_stopping_rounds,
		                 print_per_rounds,
		                 device
		                 )
	
	def train(self, model, X, y, collate_fn=None):
		if isinstance(X, (List, np.ndarray)):
			X = torch.tensor(X, dtype=torch.float)
		if isinstance(y, (List, np.ndarray)):
			y = torch.tensor(y, dtype=torch.long)
		
		return super().train(model, TensorDataset(X, y), collate_fn)


class ClassTrainer:
	
	def __init__(self,
	             max_iter=100, optimizer=optim.AdamW, learning_rate=0.001, T_max: int = 0,
	             batch_size=32, eval_batch_size=64,
	             num_workers=0, num_eval_workers=0,
	             pin_memory: bool = False, pin_memory_device: str = "",
	             persistent_workers: bool = False,
	             early_stopping_rounds: int = 10,  # 早停，等10轮决策，评价指标不在变化，停止
	             print_per_rounds: int = 1,
	             device=torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
	             ):
		self.max_iter = max_iter
		self.optimizer = optimizer
		self.learning_rate = learning_rate
		self.T_max = T_max
		self.batch_size = batch_size
		self.eval_batch_size = eval_batch_size
		self.num_workers = num_workers
		self.num_eval_workers = num_eval_workers
		self.pin_memory = pin_memory
		self.pin_memory_device = pin_memory_device
		self.persistent_workers = persistent_workers
		self.early_stopping_rounds = early_stopping_rounds
		self.print_per_rounds = print_per_rounds
		self.device = device
	
	def train(self, model, train_set: Dataset, eval_set: Dataset, collate_fn=None):
		train_loader = DataLoader(dataset=train_set, batch_size=self.batch_size, pin_memory=self.pin_memory,
		                          pin_memory_device=self.pin_memory_device, persistent_workers=self.persistent_workers,
		                          num_workers=self.num_workers, shuffle=True, collate_fn=collate_fn)
		eval_loader = DataLoader(dataset=eval_set, batch_size=self.eval_batch_size,
		                         num_workers=self.num_eval_workers, collate_fn=collate_fn)
		if self.T_max and self.T_max > 0:
			scheduler = CosineAnnealingLR(self.optimizer, T_max=self.T_max)
			return self._train_scheduler(model, train_loader, eval_loader, scheduler)
		return self._train(model, train_loader, eval_loader)
	
	def _train(self, model, train_loader: DataLoader, eval_loader: DataLoader):
		cnt = 0
		cnt2 = 0
		best_acc = 0.0
		last_acc = 0.0
		min_loss = 1000000.0
		best_model = None
		optimizer = self.optimizer(model.parameters(), lr=self.learning_rate)
		for epoch in range(self.max_iter):
			total = 0.0
			losses = 0.0
			correct = 0.0
			model.train()
			for batch in train_loader:
				batch = [x.to(self.device) for x in batch]
				# batch = [x.to(self.device) if torch.is_tensor(x) else x for x in batch]
				y = batch[1]
				logits, loss = model(*batch)
				optimizer.zero_grad()
				loss.backward()
				optimizer.step()
				
				losses += loss.item()
				correct += (logits.argmax(1) == y).sum().item()
				total += len(y)
			
			val_loss, val_acc = evaluate(model, eval_loader, self.device)
			if self.print_per_rounds == 1:
				self.print(epoch, optimizer.param_groups[0]["lr"], losses / total, correct / total, val_loss, val_acc)
			elif self.print_per_rounds > 1:
				if epoch % self.print_per_rounds == 0:
					self.print(epoch, optimizer.param_groups[0]["lr"], losses / total, correct / total, val_loss, val_acc)
			
			if val_acc - best_acc > E_CLASS or (abs(val_acc - best_acc) < E_CLASS and val_loss < min_loss):
				best_acc = val_acc
				best_model = model
				cnt = 0
				cnt2 = 0
				last_acc = val_acc
				best_acc = max(best_acc, val_acc)
				min_loss = min(min_loss, val_loss)
				continue
			
			# x次epoch的val_acc不提升或x次epoch的val_acc不变化
			if epoch >= min(5, self.early_stopping_rounds) and max(cnt, cnt2) >= self.early_stopping_rounds:
				log_utils.info(f"Early stopping at epoch-{epoch}/{self.max_iter}")
				break
			
			if abs(last_acc - val_acc) < E_CLASS:  # val_acc不在变化
				cnt2 += 1
			else:
				cnt2 = 0
			
			cnt += 1
			last_acc = val_acc
			best_acc = max(best_acc, val_acc)
			min_loss = min(min_loss, val_loss)
		
		return best_model
	
	def _train_scheduler(self, model, train_loader: DataLoader, eval_loader: DataLoader, scheduler: CosineAnnealingLR):
		cnt = 0
		cnt2 = 0
		best_acc = 0.0
		last_acc = 0.0
		min_loss = 1000000.0
		best_model = None
		optimizer = self.optimizer(model.parameters(), lr=self.learning_rate)
		for epoch in range(self.max_iter):
			total = 0.0
			losses = 0.0
			correct = 0.0
			model.train()
			for batch in train_loader:
				batch = [x.to(self.device) for x in batch]
				# batch = [x.to(self.device) if torch.is_tensor(x) else x for x in batch]
				y = batch[1]
				logits, loss = model(*batch)
				optimizer.zero_grad()
				loss.backward()
				optimizer.step()
				scheduler.step()
				
				losses += loss.item()
				correct += (logits.argmax(1) == y).sum().item()
				total += len(y)
			
			val_loss, val_acc = evaluate(model, eval_loader, self.device)
			if self.print_per_rounds == 1:
				self.print(epoch, optimizer.param_groups[0]["lr"], losses / total, correct / total, val_loss, val_acc)
			elif self.print_per_rounds > 1:
				if epoch % self.print_per_rounds == 0:
					self.print(epoch, optimizer.param_groups[0]["lr"], losses / total, correct / total, val_loss,
					           val_acc)
			
			if val_acc - best_acc > E_CLASS or (abs(val_acc - best_acc) < E_CLASS and val_loss < min_loss):
				best_acc = val_acc
				best_model = model
				cnt = 0
				cnt2 = 0
				last_acc = val_acc
				best_acc = max(best_acc, val_acc)
				min_loss = min(min_loss, val_loss)
				continue
			
			# x次epoch的val_acc不提升或x次epoch的val_acc不变化
			if epoch >= min(5, self.early_stopping_rounds) and max(cnt, cnt2) >= self.early_stopping_rounds:
				log_utils.info(f"Early stopping at epoch-{epoch}/{self.max_iter}")
				break
			
			if abs(last_acc - val_acc) < E_CLASS:  # val_acc不在变化
				cnt2 += 1
			else:
				cnt2 = 0
			
			cnt += 1
			last_acc = val_acc
			best_acc = max(best_acc, val_acc)
			min_loss = min(min_loss, val_loss)
		
		return best_model
	
	def print(self, epoch, lr, loss, correct, val_loss, val_acc):
		log_utils.info(
			f'epoch-{epoch}/{self.max_iter}  lr: {lr:.6f}, train_loss: {loss:.4f}, train_acc: {correct:.4f}, '
			f'val_loss: {val_loss:.4f}, val_acc: {val_acc:.4f}')


class SimpleClassTrainer(ClassTrainer):
	
	def __init__(self, max_iter=100, optimizer=optim.AdamW, learning_rate=0.001, T_max: int = 0,
	             batch_size=32, eval_batch_size=64,
	             num_workers=0, num_eval_workers=0,
	             pin_memory: bool = False, pin_memory_device: str = "",
	             persistent_workers: bool = False,
	             early_stopping_rounds=10,  # 早停，等10轮决策，评价指标不在变化，停止
	             print_per_rounds: int = 1,
	             device=torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')):
		super().__init__(max_iter,
		                 optimizer,
		                 learning_rate,
		                 T_max,
		                 batch_size,
		                 eval_batch_size,
		                 num_workers,
		                 num_eval_workers,
		                 pin_memory,
		                 pin_memory_device,
		                 persistent_workers,
		                 early_stopping_rounds,
		                 print_per_rounds,
		                 device
		                 )
	
	def train(self, model, X, y, eval_data: Tuple, collate_fn=None):
		if isinstance(X, (List, np.ndarray)):
			X = torch.tensor(X, dtype=torch.float)
		if isinstance(y, (List, np.ndarray)):
			y = torch.tensor(y, dtype=torch.long)
		X_val, y_val = eval_data[0], eval_data[1]
		if isinstance(X_val, (List, np.ndarray)):
			X_val = torch.tensor(X_val, dtype=torch.float)
		if isinstance(y_val, (List, np.ndarray)):
			y_val = torch.tensor(y_val, dtype=torch.long)
		
		return super().train(model, TensorDataset(X, y), TensorDataset(X_val, y_val), collate_fn)


class SplitClassTrainer(SimpleClassTrainer):
	
	def __init__(self, max_iter=100, optimizer=optim.AdamW, learning_rate=0.001, T_max: int = 0,
	             batch_size=32, eval_batch_size=64,
	             num_workers=0, num_eval_workers=0,
	             pin_memory: bool = False, pin_memory_device: str = "",
	             persistent_workers: bool = False,
	             early_stopping_rounds=10,  # 早停，等10轮决策，评价指标不在变化，停止
	             print_per_rounds: int = 1,
	             device=torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')):
		super().__init__(max_iter,
		                 optimizer,
		                 learning_rate,
		                 T_max,
		                 batch_size,
		                 eval_batch_size,
		                 num_workers,
		                 num_eval_workers,
		                 pin_memory,
		                 pin_memory_device,
		                 persistent_workers,
		                 early_stopping_rounds,
		                 print_per_rounds,
		                 device
		                 )
	
	def train(self, model, X, y, eval_size=0.2, random_state=None, collate_fn=None):
		X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=eval_size, random_state=random_state)
		return super().train(model, X_train, y_train, (X_test, y_test), collate_fn)
