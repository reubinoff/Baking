class Ingredient {
  final String name;
  final int id;
  final int quantity;
  final String units;
  final String type;

  const Ingredient(
      {required this.name,
      required this.id,
      required this.quantity,
      required this.units,
      required this.type});

  factory Ingredient.fromJson(Map<String, dynamic> json) {
    return Ingredient(
      name: json['name'],
      id: json['id'],
      quantity: json['quantity'],
      units: json['units'],
      type: json['type'],
    );
  }
}
