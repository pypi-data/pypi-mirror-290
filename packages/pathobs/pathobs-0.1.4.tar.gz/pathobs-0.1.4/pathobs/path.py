class Path:
  def __init__(self):
    self.points = []

  def add_point(self, point):
    """Adiciona um ponto ao caminho."""
    self.points.append(point)

  def get_path(self):
    """Retorna a lista de pontos do caminho."""
    return self.points

  def get_path_xy(self):
    """Retorna as coordenadas x e y do caminho."""
    return zip(*[(p.x, p.y) for p in self.points])

  def length(self):
    """Retorna o comprimento do caminho."""
    return len(self.points)

  def plot_path(self, ax=None):
    """Plota o caminho no gráfico."""
    if ax is None:
        fig, ax = plt.subplots()
    x, y = zip(*[(p.x, p.y) for p in self.points])
    ax.plot(x, y, color='blue', linewidth=2, label='Path')
  
  def total_distance(self):
    """Calcula a distância total do caminho."""
    return PathAnalyzer.total_distance(self)

  def path_smoothness(self):
    """Calcula o nível de suavidade do caminho (baseado na mudança de ângulo)."""
    return PathAnalyzer.path_smoothness(self)
  
  def acc_jerk(self):
    """Calcula a posição inversa dos pontos do caminho."""
    return PathAnalyzer.acc_jerk(self.get_path())