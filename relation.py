import re

# relation.py
class Relation:
    def __init__(self, name, attributes, tuples):
        self.name = name
        self.attributes = attributes
        self.tuples = [tuple(t) for t in tuples]

    def select(self, condition):
        # Replace standalone '=' with '==' for comparison, avoiding changing '!='
        condition = re.sub(r"(?<!\!)=(?!=)", "==", condition)

        # Modify the condition string to match tuple indices
        for i, attr in enumerate(self.attributes):
            condition = condition.replace(attr, f't[{i}]')

        # Evaluate the modified condition for each tuple
        filtered_tuples = [t for t in self.tuples if eval(condition)]
        return Relation(self.name, self.attributes, filtered_tuples)

    def project(self, attributes):
        attr_indices = [self.attributes.index(attr) for attr in attributes]
        projected_tuples = [[t[i] for i in attr_indices] for t in self.tuples]
        return Relation(self.name, attributes, projected_tuples)

    def join(self, other_relation):
        # Find common attributes for the natural join
        common_attrs = set(self.attributes).intersection(other_relation.attributes)
        
        # Create a join condition function for common attributes
        def join_condition(t1, t2):
            return all(t1[self.attributes.index(attr)] == t2[other_relation.attributes.index(attr)] for attr in common_attrs)

        # Perform the natural join operation
        joined_attributes = [attr for attr in self.attributes]
        joined_attributes += [attr for attr in other_relation.attributes if attr not in common_attrs]
        joined_tuples = []

        for t1 in self.tuples:
            for t2 in other_relation.tuples:
                if join_condition(t1, t2):
                    # Combine t1 and t2 while avoiding duplicate columns
                    joined_tuple = tuple(t1) + tuple(t2[other_relation.attributes.index(attr)] for attr in other_relation.attributes if attr not in common_attrs)
                    joined_tuples.append(joined_tuple)

        return Relation(f"{self.name}_join_{other_relation.name}", joined_attributes, joined_tuples)


    def union(self, other_relation):
        # union logic
        if self.attributes != other_relation.attributes:
            raise ValueError("Relations do not have the same schema for union")
        union_tuples = list(set(self.tuples + other_relation.tuples))
        return Relation(f"{self.name}_union_{other_relation.name}", self.attributes, union_tuples)

    def set_difference(self, other_relation):
        # set difference logic
        difference_tuples = [t for t in self.tuples if t not in other_relation.tuples]
        return Relation(f"{self.name}_difference_{other_relation.name}", self.attributes, difference_tuples)

    def intersection(self, other_relation):
        # intersection logic
        intersection_tuples = [t for t in self.tuples if t in other_relation.tuples]
        return Relation(f"{self.name}_intersection_{other_relation.name}", self.attributes, intersection_tuples)

    def __str__(self):
        return f"{self.name} ({', '.join(self.attributes)}) = {{{'; '.join([', '.join(map(str, t)) for t in self.tuples])}}}"