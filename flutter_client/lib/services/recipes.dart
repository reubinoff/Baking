import 'dart:convert';
import 'package:baking_client/services/config.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:baking_client/models/recipe.dart';

class RecipeNotifier extends ValueNotifier<List<Recipe>> {
  RecipeNotifier({
    required this.query,
  }) : super([]);

  final String query;

  int _page = 1;
  bool _hasMoreRecipe = true;
  final int _itemsPerPage = 5;
  final BakingUrl _url = BakingUrl();

  List<Recipe> _listRecipes = [];
  bool _loading = false;

  bool get loading => _loading;

  @override
  List<Recipe> get value => _value;
  List<Recipe> _value = [];

  @override
  set value(List<Recipe> newValue) {
    _value = newValue;
    notifyListeners();
  }

  Future<void> reload() async {
    _value = [];

    _listRecipes = <Recipe>[];
    _hasMoreRecipe = true;
    _page = 1;
    try {
      await httpGetRecipe(_page);
    } catch (e) {
      debugPrint(e.toString());
      debugPrintStack();
    }
  }

  Future<void> getMore() async {
    if (_hasMoreRecipe && !_loading) {
      _loading = true;
      try {
        await httpGetRecipe(_page);
      } catch (e) {
        debugPrint(e.toString());
        debugPrintStack();
      }
      _loading = false;
    }
  }

  List<Recipe> _parseRecipe(String responseBody) {
    final data = json.decode(responseBody)['items'] as List<dynamic>;
    if (data.isEmpty) {
      return [];
    }
    final parsed = data.cast<Map<String, dynamic>>();

    return parsed.map<Recipe>((json) => Recipe.fromJson(json)).toList();
  }

  Future<void> httpGetRecipe(int page) async {
    Map<String, String> queryParameters = {
      'page': _page.toString(),
      'itemsPerPage': _itemsPerPage.toString(),
    };
    if (query.isNotEmpty) {
      queryParameters['q'] = query;
    }
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
