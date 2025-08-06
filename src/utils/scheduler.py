import threading
import time
from datetime import datetime, time as dt_time
from typing import Callable, Dict, Any

from services.alert_service import AlertService
from services.ata_service import AtaService

class TaskScheduler:
    """Agendador de tarefas para verificações automáticas"""
    
    def __init__(self, ata_service: AtaService, alert_service: AlertService):
        self.ata_service = ata_service
        self.alert_service = alert_service
        self.running = False
        self.thread = None
        self.tasks = {}
        
    def start(self):
        """Inicia o agendador"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run_scheduler, daemon=True)
            self.thread.start()
            print("📅 Agendador de tarefas iniciado")
    
    def stop(self):
        """Para o agendador"""
        self.running = False
        if self.thread:
            self.thread.join()
        print("📅 Agendador de tarefas parado")
    
    def _run_scheduler(self):
        """Loop principal do agendador"""
        last_daily_check = None
        last_weekly_check = None
        last_monthly_check = None
        
        while self.running:
            try:
                now = datetime.now()
                current_date = now.date()
                current_time = now.time()
                
                # Verificação diária às 09:00
                if (current_time >= dt_time(9, 0) and 
                    current_time <= dt_time(9, 5) and 
                    last_daily_check != current_date):
                    
                    self._executar_verificacao_diaria()
                    last_daily_check = current_date
                
                # Verificação semanal (segunda-feira às 08:00)
                if (now.weekday() == 0 and  # Segunda-feira
                    current_time >= dt_time(8, 0) and 
                    current_time <= dt_time(8, 5) and 
                    last_weekly_check != current_date):
                    
                    self._executar_verificacao_semanal()
                    last_weekly_check = current_date
                
                # Verificação mensal (primeiro dia do mês às 07:00)
                if (now.day == 1 and 
                    current_time >= dt_time(7, 0) and 
                    current_time <= dt_time(7, 5) and 
                    last_monthly_check != current_date):
                    
                    self._executar_verificacao_mensal()
                    last_monthly_check = current_date
                
                # Aguarda 5 minutos antes da próxima verificação
                time.sleep(300)  # 5 minutos
                
            except Exception as e:
                print(f"Erro no agendador: {e}")
                time.sleep(60)  # Aguarda 1 minuto em caso de erro
    
    def _executar_verificacao_diaria(self):
        """Executa verificação diária de alertas"""
        try:
            print(f"\n🔍 Executando verificação diária - {datetime.now().strftime('%d/%m/%Y %H:%M')}")
            
            atas = self.ata_service.listar_todas()
            resultado = self.alert_service.verificar_alertas_automaticos(atas)
            
            print(f"✅ Verificação diária concluída:")
            print(f"   - Alertas enviados: {resultado['alertas_enviados']}")
            print(f"   - Atas alertadas: {len(resultado['atas_alertadas'])}")
            
            if resultado['erros']:
                print(f"   - Erros: {len(resultado['erros'])}")
                for erro in resultado['erros']:
                    print(f"     • {erro}")
            
            # Limpa histórico antigo
            self.alert_service.limpar_historico_antigo()
            
        except Exception as e:
            print(f"Erro na verificação diária: {e}")
    
    def _executar_verificacao_semanal(self):
        """Executa verificação semanal e envia relatório"""
        try:
            print(f"\n📊 Executando verificação semanal - {datetime.now().strftime('%d/%m/%Y %H:%M')}")
            
            atas = self.ata_service.listar_todas()
            
            # Envia relatório semanal
            if self.alert_service.enviar_relatorio_semanal(atas):
                print("✅ Relatório semanal enviado com sucesso")
            else:
                print("❌ Erro ao enviar relatório semanal")
            
            # Verifica atas críticas
            atas_criticas = self.alert_service.verificar_atas_criticas(atas)
            if atas_criticas:
                print(f"⚠️ Encontradas {len(atas_criticas)} atas críticas:")
                for item in atas_criticas:
                    ata = item["ata"]
                    criticidade = item["criticidade"]
                    print(f"   - {ata.numero_ata}: {criticidade['motivo']} (Nível: {criticidade['nivel']})")
            
        except Exception as e:
            print(f"Erro na verificação semanal: {e}")
    
    def _executar_verificacao_mensal(self):
        """Executa verificação mensal e gera relatório detalhado"""
        try:
            print(f"\n📈 Executando verificação mensal - {datetime.now().strftime('%d/%m/%Y %H:%M')}")
            
            atas = self.ata_service.listar_todas()
            
            # Gera relatório mensal
            if self.alert_service.enviar_relatorio_mensal(atas):
                print("✅ Relatório mensal gerado com sucesso")
            else:
                print("❌ Erro ao gerar relatório mensal")
            
        except Exception as e:
            print(f"Erro na verificação mensal: {e}")
    
    def executar_verificacao_manual(self) -> Dict[str, Any]:
        """Executa verificação manual de alertas"""
        try:
            print(f"\n🔍 Executando verificação manual - {datetime.now().strftime('%d/%m/%Y %H:%M')}")
            
            atas = self.ata_service.listar_todas()
            resultado = self.alert_service.verificar_alertas_automaticos(atas)
            
            print(f"✅ Verificação manual concluída:")
            print(f"   - Alertas enviados: {resultado['alertas_enviados']}")
            print(f"   - Atas alertadas: {len(resultado['atas_alertadas'])}")
            
            if resultado['erros']:
                print(f"   - Erros: {len(resultado['erros'])}")
            
            return resultado
            
        except Exception as e:
            print(f"Erro na verificação manual: {e}")
            return {"alertas_enviados": 0, "atas_alertadas": [], "erros": [str(e)]}
    
    def gerar_relatorio_manual(self, tipo: str = "semanal") -> bool:
        """Gera relatório manual"""
        try:
            atas = self.ata_service.listar_todas()
            
            if tipo == "semanal":
                return self.alert_service.enviar_relatorio_semanal(atas)
            elif tipo == "mensal":
                return self.alert_service.enviar_relatorio_mensal(atas)
            else:
                print(f"Tipo de relatório inválido: {tipo}")
                return False
                
        except Exception as e:
            print(f"Erro ao gerar relatório manual: {e}")
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna status do agendador"""
        return {
            "running": self.running,
            "thread_alive": self.thread.is_alive() if self.thread else False,
            "historico_alertas": len(self.alert_service.get_historico_alertas()),
            "ultima_verificacao": datetime.now().strftime('%d/%m/%Y %H:%M')
        }

