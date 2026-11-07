import 'package:flutter/material.dart';

class Trang1 extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    // TODO: implement build

    return Column(
      children: [
        Image.network(
          "https://images2.thanhnien.vn/528068263637045248/2024/1/25/c3c8177f2e6142e8c4885dbff89eb92a-65a11aeea03da880-1706156293184503262817.jpg?_gl=1*14ldb91*_ga*MTQ5MjUwOTAxNi4xNzk0MDQwNjc1*_ga_DDKGVNZ9BG*czE3OTQwNDA2NzQkbzEkZzAkdDE3OTQwNDA2NzQkajYwJGwwJGgw",
        ),

        Text("Xin chào các bạn UEH!"),
      ],
    );
  }
}
