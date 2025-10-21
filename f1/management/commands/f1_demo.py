from django.core.management.base import BaseCommand
from f1.repositories import F1Repository


class Command(BaseCommand):

    def handle(self, *args, **options):
        repo = F1Repository()
        # results = repo.results.model.objects.filter(driver_id=1)

        while True:
            print("\n===== Formula 1 Database Menu =====")
            print("1. Show all teams")
            print("2. Show all drivers")
            print("3. Show all circuits")
            print("4. Add new team")
            print("5. Show races results")
            print("6. Search by ID")
            print("7. Delete record by ID")
            print("0. Exit")

            choice = input("\nChoose: ")

            # 1. Всі команди
            if choice == "1":
                print("\n--- Teams List ---")
                for t in repo.teams.list_all():
                    print(f"[{t.team_id}] {t.team_name} ({t.base_country})")

            # 2. Всі пілоти
            elif choice == "2":
                print("\n--- Drivers List ---")
                for d in repo.drivers.list_all():
                    print(f"[{d.driver_id}] {d.first_name} {d.last_name} ({d.nationality})")

            # 3. Траси
            elif choice == "3":
                print("\n--- Circuits List ---")
                for c in repo.circuits.list_all():
                    print(f"[{c.circuit_id}] {c.circuit_name} — {c.country}, {c.length_km} км")

            # 4. Додавання
            elif choice == "4":
                print("\n--- New team adding ---")
                name = input("Enter team name: ")
                country = input("Enter country: ")
                new_team = repo.teams.add(team_name=name, base_country=country)
                print(f"Team added!!: [{new_team.team_id}] {new_team.team_name} ({new_team.base_country})")

            # 5. Результати
            elif choice == "5":
                print("\n--- Races results ---")
                results = repo.results.list_all().select_related('driver', 'race__circuit')[:10]

                for r in results:
                    circuit_name = r.race.circuit.circuit_name if r.race and r.race.circuit else "Unknown circuit"
                    driver_name = f"{r.driver.first_name} {r.driver.last_name}" if r.driver else "Unknown driver"
                    team_name = "Unknown Team"
                    dts = repo.driver_team_season.model.objects.filter(driver=r.driver).first()
                    if dts and dts.team:
                        team_name = dts.team.team_name
                    print(f"{circuit_name} | {driver_name} ({team_name}) — Pos: {r.position}, Points: {r.points}")

            # 6. Пошук по ID
            elif choice == "6":
                print("\n--- Search by ID ---")
                print("a) Team")
                print("b) Driver")
                print("c) Circuit")
                print("d) Races result")
                sub = input("Choose (a/b/c/d): ").lower()

                if sub == "a":
                    id_ = int(input("Enter team ID: "))
                    team = repo.teams.get_by_id(id_)
                    if team:
                        print(f"Found: [{team.team_id}] {team.team_name} ({team.base_country})")
                    else:
                        print("Error: Team not found!")

                elif sub == "b":
                    id_ = int(input("Enter driver ID: "))
                    driver = repo.drivers.get_by_id(id_)
                    if driver:
                        print(f"Found: {driver.first_name} {driver.last_name}, {driver.nationality}")
                    else:
                        print("Error: Driver not found!")

                elif sub == "c":
                    id_ = int(input("Enter circuit ID: "))
                    circuit = repo.circuits.get_by_id(id_)
                    if circuit:
                        print(f"Found: {circuit.circuit_name} ({circuit.country}), {circuit.length_km} км")
                    else:
                        print("Error: Circuit not found!")

                elif sub == "d":
                    id_ = int(input("Enter race ID: "))
                    r = repo.results.get_by_id(id_)
                    if r:
                        circuit_name = r.race.circuit.circuit_name if r.race and r.race.circuit else "Невідома траса"
                        driver_name = f"{r.driver.first_name} {r.driver.last_name}" if r.driver else "Невідомий пілот"
                        print(f"Founded: {circuit_name} | {driver_name} — Pos: {r.position}, Points: {r.points}")
                    else:
                        print("Error: Race not found!")
            elif choice == "7":
                print("\n--- Delete by ID ---")
                print("a) Team")
                print("b) Driver")
                print("c) Circuit")
                sub = input("Choose (a/b/c): ").lower()

                if sub == "a":
                    id_ = int(input("Enter team ID to delete: "))
                    if repo.teams.delete_by_id(id_):
                        print("Team deleted successfully!")
                    else:
                        print("Error: Team not found!")

                elif sub == "b":
                    id_ = int(input("Enter driver ID to delete: "))
                    if repo.drivers.delete_by_id(id_):
                        print("Driver deleted successfully!")
                    else:
                        print("Error: Driver not found!")

                elif sub == "c":
                    id_ = int(input("Enter circuit ID to delete: "))
                    if repo.circuits.delete_by_id(id_):
                        print("Circuit deleted successfully!")
                    else:
                        print("Error: Circuit not found!")


            # 0. Вихід
            elif choice == "0":
                print("\nProgram successfully finished!")
                break

            else:
                print("Error: Unknown command!")

