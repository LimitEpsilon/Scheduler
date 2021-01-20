from math import floor


class Scheduler:

  def __init__(self):
    self.no_date = int(input("이번 달은 며칠입니까?: ").strip())
    self.no_people = int(input("몇 명이서 일합니까?: ").strip())
    self.D = int(input("이번 달은 어느 요일에 시작합니까? (0: 일요일): ").strip())
    limit_d = int(input("주간은 최대 몇 번 연속해서 할 수 있습니까?: ").strip()) - 1
    limit_n = int(input("야간은 최대 몇 번 연속해서 할 수 있습니까?: ").strip()) - 1
    limit_o = int(input("초과근무는 몇 시간 미만으로 설정할까요?: ").strip())
    self.limit = [limit_d, limit_n, limit_o]
    self.holidays = [
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0
    ]
    self.vacation = []
    for i in range(self.no_people):
      self.vacation.append([
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0
      ])
    self.schedule = []
    for l in range(self.no_date * 2):
      self.schedule.append(-1)

    h = list(
      map(int, input("이번 달에 휴일은 무슨 날짜에 있습니까? (콤마 없이): ").strip().split()))
    v = []
    for ppl in range(self.no_people):
      v.append(
        list(
          map(int,
              input(str(ppl) + "번째 사람은 무슨 날짜에 휴가를 갑니까? (콤마 없이): ").strip()
              .split())))
    for date in h:
      self.holidays[date - 1] = 1
    for ppl in range(self.no_people):
      for date in v[ppl]:
        self.vacation[ppl][date - 1] = 1
    self.sat = [[], []]  #토야 is special
    p = self.no_people - 1  #assign backwards
    for date in range(self.no_date):
      self.sat[0].append(False)
      self.sat[0].append(False)
      self.sat[1].append(False)
      self.sat[1].append(False)
      if self.rests_on(date) and self.rests_on(date + 1) and (
          not self.rests_on(date + 2)):
        self.sat[0][2 * date + 1] = True
        self.schedule[2 * date + 1] = p
        p -= 1

  def test_wed(self, p):
    n = 0
    for date in range(self.no_date):
      if ((date + self.D) % 7 == 3) and (self.holidays[date] == 0) and (
          self.schedule[2 * date] == p):
        n += 1
    return (n < 2)

  def rests_on(self, d):
    return (self.holidays[d] != 0) or ((d + self.D) % 7 == 6) or (
      (d + self.D) % 7 == 0)

  def overwork(self, p):
    time = 0
    for date in range(self.no_date):
      if self.schedule[2 * date] == p:
        if self.rests_on(date):
          time += 9
        else:
          time += 1
      elif self.schedule[2 * date + 1] == p:
        if self.rests_on(date):
          if self.rests_on(date + 1):
            time += 15
          else:
            time += 7
        else:
          if self.rests_on(date + 1):
            time += 7
          else:
            time -= 1
    return time

  def test_alt(self, l):
    i = l - 1
    state = l % 2
    counter = [0, 0]
    while 0 <= i:
      if self.schedule[i] == self.schedule[l]:
        if i % 2 == state:
          if counter[state] < self.limit[state]:
            counter[state] += 1
          else:
            return False
        else:
          counter[state] = 0
          state = 1 - state
      i -= 1
    return True

  def test(self, l):
    schedule = self.schedule
    vacation = self.vacation
    if not self.test_alt(l):
      return False
    if l % 2 == 0:
      return (schedule[l - 1] != schedule[l]) and (
        schedule[l - 2] != schedule[l]) and (
          schedule[l - 3] != schedule[l]) and (
            vacation[schedule[l]][floor(l / 2)] == 0) and (
              self.overwork(schedule[l]) <
              self.limit[2]) and self.test_wed(schedule[l])
    else:
      return (schedule[l - 1] != schedule[l]) and (
        schedule[l - 2] != schedule[l]) and (
          schedule[l - 3] != schedule[l]) and (
            schedule[l - 4] != schedule[l]) and (
              vacation[schedule[l]][floor(l / 2)] == 0) and (
                self.overwork(schedule[l]) < self.limit[2])

  def print_schedule(self):
    for i in range(self.D):
      print("   |", end="")
    for date in range(self.no_date):
      if (date + self.D) % 7 == 0:
        print("\n--------------------------\n", end="")
      print(
        str(self.schedule[2 * date]) + " " + str(self.schedule[2 * date + 1]) +
        "|",
        end="")
    print()
    for ppl in range(self.no_people):
      print(str(ppl) + ": " + str(self.overwork(ppl)))

  def scheduler(self):
    l = 0
    while True:
      while 0 <= l and l < self.no_date * 2:
        if self.sat[0][l]:
          if self.sat[1][l]:
            self.sat[1][l] = False
            l -= 1
            continue
          else:
            self.sat[1][l] = True
        else:
          self.schedule[l] += 1
        if self.schedule[l] < self.no_people:
          if self.test(l):
            l += 1
        else:
          print("\rlevel " + str(l) + " terminated", end='')
          if not self.sat[0][l]: self.schedule[l] = -1
          l -= 1
      if l < 0:
        print("No more schedules.")
        break
      else:
        print()
        self.print_schedule()
        print("\n")
        l -= 1


s = Scheduler()
s.scheduler()

