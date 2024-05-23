import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('datasets/data.csv')
df_raw = pd.read_csv('datasets/data_raw.csv')


st.title("Исследование надежности заемщиков")


st.markdown("## **Цели проекта**")
st.markdown("- Определить существует ли зависимость возврата кредита в срок от семейного и финансового положения, цели получения кредита и количества детей;\
            \n- Рассчитать среднюю долю должников в каждой категории;\
            \n- Сформулировать вывод о надежности заемщиков.")



st.markdown("## **Описание данных**")
st.markdown("children — количество детей в семье\
            \ndays_employed — общий трудовой стаж в днях\
            \ndob_years — возраст клиента в годах\
            \neducation — уровень образования клиента\
            \neducation_id — идентификатор уровня образования\
            \nfamily_status — семейное положение\
            \nfamily_status_id — идентификатор семейного положения\
            \ngender — пол клиента\
            \nincome_type — тип занятости\
            \ndebt — имел ли задолженность по возврату кредитов\
            \ntotal_income — ежемесячный доход\
            \npurpose — цель получения кредита")


st.markdown("## **Подготовка датасета**")
st.markdown("Создадим сводную таблицу, показывающую зависимость возврата кредита в срок от количества детей. Для этого в index укажем столбец по которому необходимо сделать группировку - children, а в values столбец по которому будут производиться расчеты - debt, агрументом для атрибута aggfunc служит список функций, которые будут применены к столбцу в values. Выведем таблицу на экран.")

st.markdown("**Input:**")
st.markdown("pivot_children = df.pivot_table(index = 'children', values = 'debt', aggfunc = ['count', 'sum', 'mean']).sort_values(by = ('mean', 'debt'), ascending = False)\
            \npivot_children")


pivot_children = df.pivot_table(index = 'children', values = 'debt', aggfunc = ['count', 'sum', 'mean'])\
    .sort_values(by = ('mean', 'debt'), ascending = False)

st.markdown("**Output:**")
st.dataframe(pivot_children)

st.markdown("### **1.  Есть ли зависимость между количеством детей и возвратом кредита в срок?**")
st.markdown("Мы создали таблицу зависимости возврата кредита в срок от количества детей. Для более наглядного изображения таблицы, удалим мультииндекс и переименуем название столбцов. Обновленную таблицу выведем на экран.")

st.markdown("**Input:**")
st.markdown("pivot_children = pivot_children.droplevel(1,axis = 1)\
            \npivot_children = pivot_children.rename(columns = {'sum':'Всего должников','count':'Всего кредитополучателей','mean':'Доля должников'}\
            \npivot_children.index.rename('Количество детей', inplace = True)\
            \npivot_children")



pivot_children = pivot_children.droplevel(1,axis = 1)
pivot_children = pivot_children.rename(columns = {'sum':'Всего должников','count':'Всего кредитополучателей','mean':'Доля должников'})
pivot_children.index.rename('Количество детей', inplace = True)

st.markdown("**Output:**")
st.dataframe(pivot_children)


st.markdown("Сравним данные, где у семей нет детей и в семье есть один или два ребенка, это поможет получить нам общую информацию об отличие платежеспособности семей без детей и семей которые имеют детей.")
st.markdown("**Input:**")
st.markdown("pivot_children.head(3)")
st.markdown("**Output:**")
st.dataframe(pivot_children.head(3))

st.markdown("**Вывод:**\
            \nТеперь мы можем сделать вывод, что зависимость возврата кредита в срок от количества детей действительно существует. Так семьи, в которых 5 детей, всегда возвращают кредит в срок, но количество кредитополучателей с 5 детьми очень отличается от кредитополучателей с другим количеством детей. Поэтому возьмём выборку из предыдущего шага и посмотрим, что в семьях без детей всего 7 % должников, а в семьях, где есть дети этот процент увеличивается до 9%, но это не означает, что семьям с детьми не следует выдавать кредиты, просто у семей с детьми больше финансовых затрат, нежели у семей без детей.")


st.markdown("### **2. Есть ли зависимость между семейным положением и возвратом кредита в срок?**")
st.markdown("Выше мы выясняли зависимость возврата кредита в срок от количества детей, по аналогии посчитаем следующие показатели.")

st.markdown("**Input:**")
st.markdown("pivot_family_status = pd.pivot_table(df, index = ['family_status'], values = 'debt', aggfunc = ['sum','count','mean'])\
            \npivot_family_status = pivot_family_status.droplevel(1,axis = 1)\
            \npivot_family_status = pivot_family_status.rename(columns = {'sum':'Всего должников','count':'Всего кредитополучателей','mean':'Доля должников'})\
            \npivot_family_status.index.rename('Семейное положение', inplace = True)\
            \npivot_family_status")

pivot_family_status = pd.pivot_table(df, index = ['family_status'], values = 'debt', aggfunc = ['sum','count','mean'])
pivot_family_status = pivot_family_status.droplevel(1,axis = 1)
pivot_family_status = pivot_family_status.rename(columns = {'sum':'Всего должников','count':'Всего кредитополучателей','mean':'Доля должников'})
pivot_family_status.index.rename('Семейное положение', inplace = True)

st.markdown("**Output:**")
st.dataframe(pivot_family_status)

st.markdown('**Вывод:**\
            \nИз таблицы видно, что доля должников с семейным статусом **"вдовец/вдова"** ниже чем доля должников с другими семейными статусами. Из этого можно сделать вывод, что люди с данным семейным статусом ответственнее относятся к возврату кредита в срок. Но, если посмотреть на количество кредитополучателей с данным статусом, можно увидеть, что данный показатель является самым маленьким, поэтому не справедливо делать вывод только по данной метрике. Зато из таблицы явно видно, что кредитополучатели со статусом "не женат/не замужем" и "гражданский брак" чаще имеют задолженности по кредиту, чем люди со статусом "в разводе" и "женат/замужем".')


st.markdown("### **Есть ли зависимость между уровнем дохода и возвратом кредита в срок?**")

st.markdown("**Input:**")
st.markdown("pivot_total = pd.pivot_table(df, index = ['total_income_category'], values = 'debt', aggfunc = ['sum','count','mean'])\
            \npivot_total = pivot_total.droplevel(1,axis = 1)\
            \npivot_total = pivot_total.rename(columns = {'sum':'Всего должников','count':'Всего кредитополучателей','mean':'Доля должников'})\
            \npivot_total.index.rename('Уровень дохода', inplace = True)\
            \npivot_total")


pivot_total = pd.pivot_table(df, index = ['total_income_category'], values = 'debt', aggfunc = ['sum','count','mean'])
pivot_total = pivot_total.droplevel(1,axis = 1)
pivot_total = pivot_total.rename(columns = {'sum':'Всего должников','count':'Всего кредитополучателей','mean':'Доля должников'})
pivot_total.index.rename('Уровень дохода', inplace = True)

st.markdown("**Output:**")
st.dataframe(pivot_total)


st.markdown("Напомним, что категории соответствуют уровням дохода:\
            \n'A' — 1000001 и выше\
            \n'B' — 200001–1000000\
            \n'C' — 50001–200000\
            \n'D' — 30001–50000\
            \n'E' — 0–30000\
            \n\
            \n**Рассчитаем среднюю долю должников по всем уровням дохода:**")

st.markdown("**Input:**")
st.markdown("pivot_total['Доля должников'].mean()")

st.markdown("**Output:**")
st.markdown(pivot_total['Доля должников'].mean())

st.markdown('**Вывод:**\
            \nИз таблицы видно, что самыми малочисленными являются категории "А" и "Е", поэтому доля должников в них достаточно велика. Если же взять наиболее многочисленную категорию - "С", то можно сказать, что люди с этим уровнем дохода чаще берут кредиты и, что доля должников в ней приближается к категории "Е", что является странным для людей с данным уровнем дохода. Самыми дисциплинированными оказались люди с доходом от 30 до 50 тысяч, но их не так много. Из расчета средней доли должников по всем уровням дохода видно, что только 8 % кредитополучателей не возвращают кредит в срок, а это очень хороший результат.')


st.markdown("### **Как разные цели кредита влияют на его возврат в срок?**")

st.markdown("**Input:**")
st.markdown("pivot_purpose = pd.pivot_table(df, index = ['purpose_category'], values = 'debt', aggfunc = ['sum','count','mean'])\
            \npivot_purpose = pivot_purpose.droplevel(1,axis = 1)\
            \npivot_purpose = pivot_purpose.rename(columns = {'sum':'Всего должников','count':'Всего кредитополучателей','mean':'Доля должников'})\
            \npivot_purpose.index.rename('Цель кредита', inplace = True)\
            \npivot_purpose")

pivot_purpose = pd.pivot_table(df, index = ['purpose_category'], values = 'debt', aggfunc = ['sum','count','mean'])
pivot_purpose = pivot_purpose.droplevel(1,axis = 1)
pivot_purpose = pivot_purpose.rename(columns = {'sum':'Всего должников','count':'Всего кредитополучателей','mean':'Доля должников'})
pivot_purpose.index.rename('Цель кредита', inplace = True)


st.markdown("**Output:**")
st.dataframe(pivot_purpose)

st.markdown('**Вывод:**\
            \nИз таблицы видно, что кредит, взятый на проведение свадьбы или операции с недвижимостью, чаще возвращается людьми в срок, нежели кредит, взятый на автомобиль или образование. Это можно объяснить тем, что, когда человек приобретает автомобиль или получает образование, у него могут возникнуть дополнительные расходы, что приостанавливает возврат кредита.')


st.markdown("### **Объясните, почему заполнить пропуски медианным значением — лучшее решение для количественных переменных**")


st.markdown('***Ответ:***\
            \nПропуски в количественных переменных лучше заполнять характерными значениями, характеризующими состояние выборки, — набора данных, выбранных для проведения исследования. Чтобы примерно оценить типичные значения выборки, годятся среднее арифметическое или медиана.\
            \n- Среднее арифметическое — это сумма всех значений, поделённая на количество значений (mean()).\
            \n- Медиана — это такое число в выборке, что ровно половина элементов больше него, а другая половина — меньше (median()).\
            \n\
            \nВ данном датафрейме был выбран метод заполнения недостающих значений медианным значением, так как мы заполняли пропуски для разных категорий подчиненных и в этих категориях данные неоднородны, и среди данных есть выделяющиеся из большинства значения.')

fig = plt.figure(figsize = (15,5))

ax = df_raw['days_employed'].hist(bins = 40)

ax.axvline(x = df_raw['days_employed'].mean(), color = 'r', linestyle = 'dashed', label = 'mean')
ax.axvline(x = df_raw['days_employed'].median(), color = 'y', linestyle = 'dashed', label = 'median')
plt.legend()
plt.title('Гистограмма по столбцу days_employed с медианой и средним')

st.pyplot(fig)


st.markdown("### **Расчеты перед выводом**")

st.markdown("**Input:**")
st.markdown("conclusion = pd.DataFrame([[pivot_children['Доля должников'].mean()],\
            \n    [ pivot_family_status['Доля должников'].mean()],\
            \n    [ pivot_total['Доля должников'].mean()],\
            \n    [pivot_purpose['Доля должников'].mean()]],\
            \n  index = ['Дети','Семья','Доход','Цель'],\
            \n    columns = ['Доля должников'])\
            \nconclusion")


st.markdown("**Output:**")
conclusion = pd.DataFrame([[pivot_children['Доля должников'].mean()],
                          [ pivot_family_status['Доля должников'].mean()],
                          [ pivot_total['Доля должников'].mean()],
                          [pivot_purpose['Доля должников'].mean()]],
index = ['Дети','Семья','Доход','Цель'],
columns = ['Доля должников'])

st.dataframe(conclusion)

st.markdown("### **Общий вывод**")
st.markdown("На основе данных о статистике платёжеспособности клиентов, данных нам заказчиком, проведя работу по предобработке данных, мы исследоввали зависимость 4 критериев на возврат кредита в срок:\
            \n1. Количество детей\
            \n1. Семейное положение\
            \n1. Уровень дохода\
            \n1. Цель кредита\
\n\
\nПроведя данное исследование, можно сделать вывод:\
            \n1. Каждый из критериев влияет на возврат кредита в срок в большей или меньшей степени.\
            \n1. Доля должников по каждой категории не превышает 10 %, что указывает на надежность заемщиков.\
            \n1. Среднее значение доли должников банка по всем категориям составляет всего 8%, что говорит об ответственном отношении клиентов банка к финансам.\
            \n1. Пересмотреть градацию по доходам для получения более сбалансированной выдержки.")
