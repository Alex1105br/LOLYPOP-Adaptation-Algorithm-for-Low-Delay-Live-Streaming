class LOLYPOP:
    def __init__(self, sigma_star, omega_star):
        """
        Inicializa o algoritmo LOLYPOP com os limites fornecidos.
        
        :param sigma_star: Limite de segmentos ignorados.
        :param omega_star: Limite de transições de qualidade.
        """
        self.sigma_star = sigma_star
        self.omega_star = omega_star
        self.last_quality = 0  # Representação do último segmento baixado
    
    def select_representation(self, probabilities, current_transitions):
        """
        Seleciona a representação de qualidade para o próximo segmento.
        
        :param probabilities: Lista de probabilidades de sucesso de download para cada qualidade.
        :param current_transitions: Número atual de transições de qualidade relativas (\(Ω\)).
        :return: Índice da qualidade selecionada.
        """
        # Passo 1: Encontrar a qualidade mais alta que satisfaz o limite Σ*
        max_quality = 0
        for j, p in enumerate(probabilities):
            if p >= 1 - self.sigma_star:
                max_quality = j
        
        # Passo 2: Verificar se a transição é permitida com base em Ω*
        if current_transitions > self.omega_star and max_quality > self.last_quality:
            selected_quality = self.last_quality  # Manter a qualidade atual
        else:
            selected_quality = max_quality  # Permitir a transição
        
        # Atualizar a última qualidade e retornar
        self.last_quality = selected_quality
        return selected_quality


# Exemplo de uso
if __name__ == "__main__":
    # Parâmetros do algoritmo
    sigma_star = 0.05  # 5% de segmentos ignorados permitidos
    omega_star = 0.1   # 10% de transições de qualidade permitidas

    # Inicializa o algoritmo
    lolypop = LOLYPOP(sigma_star, omega_star)

    # Exemplo de probabilidades para diferentes representações (qualidades)
    download_probabilities = [0.8, 0.7, 0.6, 0.4]  # Probabilidades para as qualidades 0, 1, 2, 3
    current_transitions = 0.08  # Transições atuais (\(Ω\))

    # Seleciona a qualidade para o próximo segmento
    selected_quality = lolypop.select_representation(download_probabilities, current_transitions)
    print(f"Qualidade selecionada: {selected_quality}")
