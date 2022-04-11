import 'dart:convert';
import 'package:baking_client/services/config.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:baking_client/models/recipe.dart';

class RecipeNotifier extends ValueNotifier<List<Recipe>> {
  RecipeNotifier() : super([]);

  int _page = 1;
  bool _hasMoreRecipe = true;
  final int _itemsPerPage = 5;
  final BakingUrl _url = BakingUrl();

  List<Recipe> _listRecipes = [];
  bool _loading = false;

  @override
  List<Recipe> get value => _value;
  List<Recipe> _value = [];

  @override
  set value(List<Recipe> newValue) {
    _value = newValue;
    notifyListeners();
  }

  Future<void> reload() async {
    _listRecipes = <Recipe>[];
    _page = 1;
    try {
      await httpGetRecipe(_page);
    } catch (e) {
      debugPrint(e.toString());
    }
  }

  Future<void> getMore() async {
    if (_hasMoreRecipe && !_loading) {
      _loading = true;
      await httpGetRecipe(_page);
      _loading = false;
    }
  }

  List<Recipe> _parseRecipe(String responseBody) {
    final data = json.decode(responseBody)["items"] as List<dynamic>;
    if (data.isEmpty) {
      return [];
    }
    final parsed = data.cast<Map<String, dynamic>>();

    return parsed.map<Recipe>((json) => Recipe.fromJson(json)).toList();
  }

  Future<void> httpGetRecipe(int page) async {
    Map<String, String> queryParameters = {
      'page': _page.toString(),
      'itemsPerPage': _itemsPerPage.toString()
    };
    final uri = _url.createUrl('/recipe', queryParameters);
    final res = await http.get(uri);
    // debugPrint(res.body);
    List<Recipe> data = _parseRecipe(res.body);
    if (data.isEmpty) {
      _hasMoreRecipe = false;
    } else {
      _listRecipes.addAll(data);
      _page++;
    }
    value = _listRecipes;
  }
}

// class UserService {
//   final String api =
//       "https://service.baking.reubinoff.com/recipe?itemsPerPage=10";
// // final String api = "http://localhost:8888/recipe?itemsPerPage=10";

//   List<Recipe> _parseRecipe(String responseBody) {
//     final parsed =
//         jsonDecode(responseBody)["items"].cast<Map<String, dynamic>>();
//     return parsed.map<Recipe>((json) => Recipe.fromJson(json)).toList();
//   }

//   Future<List<Recipe>> _fetchData(http.Client client) async {
//     final response = await client
//         .get(Uri.parse(api), headers: {"Accept": "application/json"});
//     if (response.statusCode == 200) {
//       return _parseRecipe(response.body);
//     } else {
//       throw Exception('Failed to load recipe');
//     }
//   }

//   Future<List<Recipe>> getRecipes(int page, int itemsPerPage) async {
//     final client = http.Client();
//     final List<Recipe> recipes = await _fetchData(client);
//     return recipes;
//   }
// }
