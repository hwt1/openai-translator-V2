from book.content import Content, ContentType


class Model:
    # 为文本内容生成提示词
    def make_text_prompt(self, text: str, target_language: str) -> str:
        return f"翻译为{target_language}：{text}"

    # 为表格内容生成提示词
    def make_table_prompt(self, table: str, target_language: str) -> str:
        return f"翻译为{target_language}，直接返回结果数据，不加其他无关的文案，返回格式样例：[[ '水果', '颜色', '价格（美元）'], [ '苹果', '红色', '1.20']：\n{table}"

    # 根据 content对象获取翻译提示词
    def translate_prompt(self, content: Content, target_language: str) -> str:
        if content.content_type == ContentType.TEXT:
            return self.make_text_prompt(content.original, target_language)
        elif content.content_type == ContentType.TABLE:
            return self.make_table_prompt(content.get_original_as_str(), target_language)

    # 实际向大模型发起请求的方法
    def make_request(self, prompt):
        raise NotImplementedError("子类必须实现 make_request 方法")