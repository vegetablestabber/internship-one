# Obtain column name based on the imported MAESTRI dataset, given ICS and company role
old_col = lambda std, role: f"{std.value} code - {role} industry"

# Obtain concise column name, given ICS and company role
new_col = lambda std, role: f"{role} {std.value} code"

# Roles of companies in industrial symbiosis
new_roles = ("Donor", "Intermediary", "Receiver")