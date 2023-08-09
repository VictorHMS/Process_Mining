import csv
import random
from datetime import datetime, timedelta

START_ACTIVITY = "Solicitar atendimento"
END_ACTIVITY = "Encerrar negociação"
ACTIVITIES = ["Retirar carro", "Reservar carro", "Remover reserva", 
              "Estender aluguel",
              "Adicionar acessórios", "Devolver carro", "Alertar defeito"]

ALL = [START_ACTIVITY] + ACTIVITIES + [END_ACTIVITY]

#Regras de precedência:
#
PRECENDECE1 = {
    'Retirar carro' : START_ACTIVITY,
    'Estender aluguel' : 'Retirar carro',
    'Reservar carro' : START_ACTIVITY,
    'Adicionar acessórios' : START_ACTIVITY,
    'Alertar defeito' : 'Retirar carro',
    END_ACTIVITY : START_ACTIVITY
}

PRECENDECE2 = {
    'Devolver carro' : 'Retirar carro',
    'Remover reserva' : 'Reservar carro'
}

#Regras de Obrigação:
#
OBLIGATION = {
    'Reservar carro' : ['Remover reserva', 'Retirar carro'],
    'Retirar carro' : ['Devolver carro'],
}

#Regras de Proibição:
PROIB = {
    'Adicionar acessórios' : 'Retirar carro',
    'Extender aluguel' : 'Devolver carro'
}

RESOURCES = ["Dona Dorinha", "Douglas", "Lucio"]

CASE_COUNT = 400
START_DATE = datetime(2023, 6, 1)

CSV_PATH = "locadora.csv"
CSV_COLUMNS = ["Caso", "Atividade", "Recurso", "Início", "Fim"]
NLIM = 20

def main():
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(CSV_COLUMNS)

        for i in range(CASE_COUNT):
            
            id = i+1
            case_data = []
            ocurr = dict()
            obligationsLeft = dict()

            for atv in ALL:
                ocurr[atv] = 0
                obligationsLeft[atv] = 0

            totalActivities = 0

            start_date = START_DATE + timedelta(days=random.randint(0, 29))
            activity_duration = random.randint(15, 60)
            end_date = start_date + timedelta(minutes=activity_duration)
            recurso = random.choice(RESOURCES)
            case_data.append([id, START_ACTIVITY, recurso, start_date, end_date])
            allActiv = [START_ACTIVITY]
            ocurr[START_ACTIVITY] = 1

            while True:
                atualActiv = random.choice(ACTIVITIES + [END_ACTIVITY])
                
                #VERIFICA SE AS PRECEDENCIAS UNICAS FORAM ATENDIDAS
                
                if atualActiv in PRECENDECE1:
                    if PRECENDECE1[atualActiv] not in allActiv:
                        #precedencia nao atendida
                        continue

                
                #VERIFICA SE AS PRECEDENCIAS REPETITIVAS FORAM ATENDIDAS
                if atualActiv in PRECENDECE2:
                    if ocurr[PRECENDECE2[atualActiv]] <= ocurr[atualActiv]:
                        #precisa ocorrer a precedencia novamente
                        continue
                
                
                if atualActiv in PROIB:
                    if ocurr[PROIB[atualActiv]] > 0:
                        
                        #ATIVIDADE PROIBIDA
                        continue
                
                
                if atualActiv in OBLIGATION:
                    obli = random.choice(OBLIGATION[atualActiv])
                    obligationsLeft[obli] += 1

                if obligationsLeft[atualActiv] > 0:
                    obligationsLeft[atualActiv]  -= 1
                
                flag = 0
                if atualActiv == END_ACTIVITY:
                    for obli in obligationsLeft:
                        if(obligationsLeft[obli] > 0):
                            flag = 1
                
                if flag == 1:
                    continue

                
                ocurr[atualActiv] += 1
                allActiv.append(atualActiv)
                totalActivities += 1

                duration_between_activities = random.randint(5, 90)
                start_date = end_date + timedelta(minutes=duration_between_activities)
                activity_duration = random.randint(15, 60)
                end_date = start_date + timedelta(minutes=activity_duration)
                recurso = random.choice(RESOURCES)
                case_data.append([id, atualActiv, recurso, start_date, end_date])
                
                if atualActiv == END_ACTIVITY:
                    break

                #se o fluxo estiver muito grande, tenta chegar ao END_ACTIVITY e encerrar
                if(totalActivities >= NLIM):
                    lis = []
                    for obli in obligationsLeft:
                        if(obligationsLeft[obli] > 0):
                            lis.append(obli)
                    options = set(lis)

                    while len(options) > 0:
                        atual = random.choice(list(options))
                        allActiv.append(atual)
                        obligationsLeft[atual] -= 1
                        if obligationsLeft[atual] <= 0:
                            options.remove(atual)
                        totalActivities += 1
                        
                        if atual in OBLIGATION:
                            obli = random.choice(OBLIGATION[atual])
                            obligationsLeft[obli] += 1
                            lis = []
                            for obli in obligationsLeft:
                                if(obligationsLeft[obli] > 0):
                                    lis.append(obli)
                            options = set(lis)
                        duration_between_activities = random.randint(5, 90)
                        start_date = end_date + timedelta(minutes=duration_between_activities)
                        activity_duration = random.randint(15, 60)
                        end_date = start_date + timedelta(minutes=activity_duration)
                        recurso = random.choice(RESOURCES)
                        case_data.append([id, atual, recurso, start_date, end_date])
                    
                    atual = END_ACTIVITY
                    allActiv.append(atual)
                    totalActivities += 1

                    duration_between_activities = random.randint(5, 90)
                    start_date = end_date + timedelta(minutes=duration_between_activities)
                    activity_duration = random.randint(15, 60)
                    end_date = start_date + timedelta(minutes=activity_duration)
                    recurso = random.choice(RESOURCES)
                    case_data.append([id, atual, recurso, start_date, end_date])
                    break

                
                #lembrar de adicionar a atividade, 
                #lembrar de contar o numero de ocorrencias
            
            for row in case_data:
                writer.writerow(row)
            
            print(case_data)

if __name__ == '__main__':
    main()
