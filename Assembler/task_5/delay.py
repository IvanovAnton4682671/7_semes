
def delay(n1, n2, n3):
    #сохранение+объявление n1+(итерации внешнего цикла-1)*внутренний цикл+последняя итерация внешнего цикла+третий цикл+подгонка+восстановление+прерывание
    res = 44+4+((n1-1)*(4+(n2-1)*21+9+17)+(4+(n2-1)*21+9+5))+(4+(n3-1)*18+6)+10+36+20
    return res

if __name__ == "__main__":
    res = delay(100, 1189, 117)
    print(f"{res:,}")
