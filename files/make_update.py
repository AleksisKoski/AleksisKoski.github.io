from datetime import datetime

# Read and increment version from update.txt
with open('update.txt', 'r') as f:
    first_line = f.readline().strip()

# Extract version number assuming format "Version: x.y"
prefix, version_str = first_line.split(':')
version_str = version_str.strip()
major, minor = version_str.split('.')
minor = str(int(minor) + 1)  # increment minor version
new_version = f"{major}.{minor}"

# Get current date in day.month.year format
current_date = datetime.now().strftime("%d.%m.%Y")

old_dict = {}  # key by course code for easy lookup
new_dict = {}  # key by course code for easy lookup

class Course:
    def __init__(self, name, code, lecturer):
        self.name = name
        self.code = code
        self.lecturer = lecturer
        self.instances = []

    def add_instance(self, day, startTime, endTime, roomStr, weeks):
        self.instances.append({
            'day': day,
            'startTime': startTime,
            'endTime': endTime,
            'room': roomStr,
            'weeks': weeks
        })

    def is_equal(self, other):
        if not other:
            return False
        if (self.name != other.name or self.lecturer != other.lecturer):
            print(f"Metadata mismatch in course {self.code} {self.name}:")
            if self.name != other.name:
                print(f"  Name: {self.name} != {other.name}")
            if self.lecturer != other.lecturer:
                print(f"  Lecturer: {self.lecturer} != {other.lecturer}")
            print(" ")
            return False
        # Compare instances ignoring order
        # Convert to set of tuples for easy comparison
        def to_tuple_list(course):
            return set((i['day'], i['startTime'], i['endTime'], i['room'], i['weeks']) for i in course.instances)

        self_set = to_tuple_list(self)
        other_set = to_tuple_list(other)

        if self_set != other_set:
            print(f"Instance mismatch in course {self.code} {self.name}:")
            only_in_self = self_set - other_set
            only_in_other = other_set - self_set

            if only_in_self:
                print("  Present only in new version:")
                for instance in only_in_self:
                    print(f"    {instance}")
            if only_in_other:
                print("  Present only in old version:")
                for instance in only_in_other:
                    print(f"    {instance}")
            print(" ")
            return False

        return True


with open('oldcourses.txt', 'r') as f:
    f.readline()
    for line in f:
        data = line.strip().split(';')
        if len(data)>26:
            name = data[1]
            code = data[2]
            lecturer = data[26]
            weeks = data[11]

            day = data[3]
            startTime = data[4]
            endTime = data[5]
            roomStr = data[7]

            if code not in old_dict:
                old_dict[code] = Course(name, code, lecturer)

            old_dict[code].add_instance(day, startTime, endTime, roomStr, weeks)
        
oldCourses = list(old_dict.values())

with open('courses.txt', 'r') as f:
    f.readline()
    for line in f:
        data = line.strip().split(';')
        if len(data)>26:
            name = data[1]
            code = data[2]
            lecturer = data[26]
            weeks = data[11]

            day = data[3]
            startTime = data[4]
            endTime = data[5]
            roomStr = data[7]

            if code not in new_dict:
                new_dict[code] = Course(name, code, lecturer)

            new_dict[code].add_instance(day, startTime, endTime, roomStr, weeks)
        
newCourses = list(new_dict.values())

updatedCourses = []
changedCourses = []

for code, new_course in new_dict.items():
    old_course = old_dict.get(code)

    if old_course is None:
        updatedCourses.append(new_course)
    else:
        if not new_course.is_equal(old_course):
            changedCourses.append(new_course)

# Write to new updates.txt
if updatedCourses or changedCourses:
    with open('update.txt', 'w') as f:
        f.write(f"version: {new_version}\n")
        f.write("**Course data updated on:**\n\n")
        f.write(f"{current_date}\n\n")
        f.write("**Added courses:**\n\n")
        if updatedCourses:
            for course in updatedCourses:
                f.write(f"{course.code} {course.name}\n")
        else: f.write(f"-\n")
        f.write("\n**Changed courses:**\n\n")
        if changedCourses:
            for course in changedCourses:
                f.write(f"{course.code} {course.name}\n")
        else: f.write(f"-\n")
