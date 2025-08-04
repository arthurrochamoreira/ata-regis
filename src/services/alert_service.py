from datetime import date, datetime, timedelta
from typing import List, Dict, Any

# Importações condicionais para suportar execução direta e como módulo
try:
    from ..models.ata import Ata
    from ..utils.email_service import EmailService
except ImportError:
    from models.ata import Ata
    from utils.email_service import EmailService

class AlertService:
    """Serviço para gerenciar alertas automáticos"""
    
    def __init__(self, email_service: EmailService):
        self.email_service = email_service
        self.alert_history = []  # Histórico de alertas enviados
    
    def verificar_alertas_automaticos(self, atas: List[Ata]) -> Dict[str, Any]:
        """Verifica e envia alertas automáticos baseado nas regras de negócio"""
        resultado = {
            "alertas_enviados": 0,
            "atas_alertadas": [],
            "erros": []
        }
        
        hoje = date.today()
        
        for ata in atas:
            dias_restantes = ata.dias_restantes
            
            # Regras de alerta automático
            deve_alertar = False
            tipo_alerta = ""
            
            # Alerta D-90 (90 dias antes do vencimento)
            if dias_restantes == 90:
                deve_alertar = True
                tipo_alerta = "D-90"
            
            # Alerta D-60 (60 dias antes do vencimento)
            elif dias_restantes == 60:
                deve_alertar = True
                tipo_alerta = "D-60"
            
            # Alerta D-30 (30 dias antes do vencimento)
            elif dias_restantes == 30:
                deve_alertar = True
                tipo_alerta = "D-30"
            
            # Alerta D-15 (15 dias antes do vencimento)
            elif dias_restantes == 15:
                deve_alertar = True
                tipo_alerta = "D-15"
            
            # Alerta D-7 (7 dias antes do vencimento)
            elif dias_restantes == 7:
                deve_alertar = True
                tipo_alerta = "D-7"
            
            # Alerta D-1 (1 dia antes do vencimento)
            elif dias_restantes == 1:
                deve_alertar = True
                tipo_alerta = "D-1"
            
            # Alerta de vencimento (no dia do vencimento)
            elif dias_restantes == 0:
                deve_alertar = True
                tipo_alerta = "VENCIMENTO"
            
            # Alerta pós-vencimento (atas vencidas)
            elif dias_restantes < 0 and dias_restantes >= -30:  # Até 30 dias após vencimento
                deve_alertar = True
                tipo_alerta = "POS-VENCIMENTO"
            
            if deve_alertar:
                # Verifica se já foi enviado alerta para esta ata hoje
                if not self._ja_alertado_hoje(ata.numero_ata, tipo_alerta):
                    try:
                        if self.email_service.enviar_alerta_vencimento(ata):
                            resultado["alertas_enviados"] += 1
                            resultado["atas_alertadas"].append({
                                "numero_ata": ata.numero_ata,
                                "tipo_alerta": tipo_alerta,
                                "dias_restantes": dias_restantes
                            })
                            
                            # Registra no histórico
                            self._registrar_alerta(ata.numero_ata, tipo_alerta)
                            
                            print(f"✅ Alerta {tipo_alerta} enviado para ata {ata.numero_ata}")
                        else:
                            resultado["erros"].append(f"Erro ao enviar alerta para ata {ata.numero_ata}")
                    except Exception as e:
                        resultado["erros"].append(f"Erro ao processar ata {ata.numero_ata}: {str(e)}")
        
        return resultado
    
    def enviar_relatorio_semanal(self, atas: List[Ata]) -> bool:
        """Envia relatório semanal das atas"""
        try:
            stats = self._calcular_estatisticas(atas)
            atas_proximas = [ata for ata in atas if 0 <= ata.dias_restantes <= 90]
            
            return self.email_service.enviar_relatorio_semanal(
                stats["vigente"],
                stats["a_vencer"],
                stats["vencida"],
                atas_proximas
            )
        except Exception as e:
            print(f"Erro ao enviar relatório semanal: {e}")
            return False
    
    def enviar_relatorio_mensal(self, atas: List[Ata]) -> bool:
        """Envia relatório mensal detalhado"""
        try:
            print(f"\n{'='*60}")
            print("RELATÓRIO MENSAL - ATAS DE REGISTRO DE PREÇOS")
            print(f"{'='*60}")
            print(f"Período: {date.today().strftime('%B/%Y')}")
            print(f"Data de Geração: {date.today().strftime('%d/%m/%Y')}")
            
            # Estatísticas gerais
            stats = self._calcular_estatisticas(atas)
            total_atas = sum(stats.values())
            total_valor = sum(ata.valor_total for ata in atas)
            
            print(f"\n📊 RESUMO EXECUTIVO:")
            print(f"- Total de Atas: {total_atas}")
            print(f"- Valor Total: R$ {total_valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
            print(f"- Vigentes: {stats['vigente']} ({(stats['vigente']/total_atas*100):.1f}%)" if total_atas > 0 else "- Vigentes: 0")
            print(f"- A Vencer: {stats['a_vencer']} ({(stats['a_vencer']/total_atas*100):.1f}%)" if total_atas > 0 else "- A Vencer: 0")
            print(f"- Vencidas: {stats['vencida']} ({(stats['vencida']/total_atas*100):.1f}%)" if total_atas > 0 else "- Vencidas: 0")
            
            # Atas por fornecedor
            fornecedores = {}
            for ata in atas:
                if ata.fornecedor not in fornecedores:
                    fornecedores[ata.fornecedor] = {"count": 0, "valor": 0}
                fornecedores[ata.fornecedor]["count"] += 1
                fornecedores[ata.fornecedor]["valor"] += ata.valor_total
            
            print(f"\n🏢 ATAS POR FORNECEDOR:")
            for fornecedor, data in sorted(fornecedores.items(), key=lambda x: x[1]["valor"], reverse=True):
                valor_formatado = f"R$ {data['valor']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                print(f"- {fornecedor}: {data['count']} ata(s) - {valor_formatado}")
            
            # Vencimentos próximos
            atas_proximas = [ata for ata in atas if 0 <= ata.dias_restantes <= 90]
            if atas_proximas:
                print(f"\n⚠️ ATAS PRÓXIMAS DO VENCIMENTO:")
                for ata in sorted(atas_proximas, key=lambda x: x.dias_restantes):
                    print(f"- {ata.numero_ata}: {ata.objeto} (vence em {ata.dias_restantes} dias)")
            
            # Atas vencidas
            atas_vencidas = [ata for ata in atas if ata.dias_restantes < 0]
            if atas_vencidas:
                print(f"\n❌ ATAS VENCIDAS:")
                for ata in sorted(atas_vencidas, key=lambda x: x.dias_restantes):
                    dias_vencida = abs(ata.dias_restantes)
                    print(f"- {ata.numero_ata}: {ata.objeto} (vencida há {dias_vencida} dias)")
            
            print(f"\n📈 ANÁLISE DE TENDÊNCIAS:")
            # Análise simples de tendências
            atas_este_ano = [ata for ata in atas if ata.data_vigencia.year == date.today().year]
            atas_proximo_ano = [ata for ata in atas if ata.data_vigencia.year == date.today().year + 1]
            
            print(f"- Atas vencendo este ano: {len(atas_este_ano)}")
            print(f"- Atas vencendo próximo ano: {len(atas_proximo_ano)}")
            
            if len(atas_este_ano) > len(atas_proximo_ano):
                print("- Tendência: Concentração de vencimentos este ano - atenção redobrada necessária")
            elif len(atas_proximo_ano) > len(atas_este_ano):
                print("- Tendência: Distribuição equilibrada de vencimentos")
            
            print(f"\n💡 RECOMENDAÇÕES:")
            if stats["a_vencer"] > 0:
                print("- Iniciar processos de renovação para atas próximas do vencimento")
            if stats["vencida"] > 0:
                print("- Regularizar situação das atas vencidas")
            if total_atas < 5:
                print("- Considerar ampliação do portfólio de atas")
            
            print(f"\nRelatório gerado automaticamente pelo Sistema de Atas de Registro de Preços")
            print(f"{'='*60}\n")
            
            return True
            
        except Exception as e:
            print(f"Erro ao gerar relatório mensal: {e}")
            return False
    
    def verificar_atas_criticas(self, atas: List[Ata]) -> List[Dict[str, Any]]:
        """Identifica atas que requerem atenção imediata"""
        atas_criticas = []
        
        for ata in atas:
            criticidade = self._avaliar_criticidade(ata)
            if criticidade["nivel"] in ["ALTA", "CRÍTICA"]:
                atas_criticas.append({
                    "ata": ata,
                    "criticidade": criticidade
                })
        
        return atas_criticas
    
    def _calcular_estatisticas(self, atas: List[Ata]) -> Dict[str, int]:
        """Calcula estatísticas das atas"""
        stats = {"vigente": 0, "a_vencer": 0, "vencida": 0}
        for ata in atas:
            stats[ata.status] += 1
        return stats
    
    def _avaliar_criticidade(self, ata: Ata) -> Dict[str, Any]:
        """Avalia o nível de criticidade de uma ata"""
        dias_restantes = ata.dias_restantes
        valor = ata.valor_total
        
        # Critérios de criticidade
        if dias_restantes < 0:
            nivel = "CRÍTICA"
            motivo = f"Ata vencida há {abs(dias_restantes)} dias"
        elif dias_restantes <= 7:
            nivel = "CRÍTICA"
            motivo = f"Vencimento em {dias_restantes} dias"
        elif dias_restantes <= 15:
            nivel = "ALTA"
            motivo = f"Vencimento em {dias_restantes} dias"
        elif dias_restantes <= 30:
            nivel = "MÉDIA"
            motivo = f"Vencimento em {dias_restantes} dias"
        elif dias_restantes <= 60:
            nivel = "BAIXA"
            motivo = f"Vencimento em {dias_restantes} dias"
        else:
            nivel = "NORMAL"
            motivo = "Ata vigente"
        
        # Ajusta criticidade baseado no valor
        if valor > 1000000:  # Atas acima de 1 milhão
            if nivel == "MÉDIA":
                nivel = "ALTA"
            elif nivel == "BAIXA":
                nivel = "MÉDIA"
        
        return {
            "nivel": nivel,
            "motivo": motivo,
            "dias_restantes": dias_restantes,
            "valor": valor
        }
    
    def _ja_alertado_hoje(self, numero_ata: str, tipo_alerta: str) -> bool:
        """Verifica se já foi enviado alerta para esta ata hoje"""
        hoje = date.today()
        for registro in self.alert_history:
            if (registro["numero_ata"] == numero_ata and 
                registro["tipo_alerta"] == tipo_alerta and 
                registro["data"] == hoje):
                return True
        return False
    
    def _registrar_alerta(self, numero_ata: str, tipo_alerta: str):
        """Registra alerta no histórico"""
        self.alert_history.append({
            "numero_ata": numero_ata,
            "tipo_alerta": tipo_alerta,
            "data": date.today(),
            "timestamp": datetime.now()
        })
        
        # Limita histórico a 1000 registros
        if len(self.alert_history) > 1000:
            self.alert_history = self.alert_history[-1000:]
    
    def get_historico_alertas(self, dias: int = 30) -> List[Dict[str, Any]]:
        """Retorna histórico de alertas dos últimos N dias"""
        data_limite = date.today() - timedelta(days=dias)
        return [
            registro for registro in self.alert_history 
            if registro["data"] >= data_limite
        ]
    
    def limpar_historico_antigo(self, dias: int = 90):
        """Remove registros de alerta mais antigos que N dias"""
        data_limite = date.today() - timedelta(days=dias)
        self.alert_history = [
            registro for registro in self.alert_history 
            if registro["data"] >= data_limite
        ]

