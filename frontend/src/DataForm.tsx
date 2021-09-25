import React from "react";
import {
  Form,
  Button,
  ConfigProvider,
  DatePicker,
  Radio,
  Select,
  Spin,
  List,
  notification,
} from "antd";
import locale from "antd/lib/locale/ko_KR";
import { locations } from "./locations";
import { LoadingOutlined } from "@ant-design/icons";

const { RangePicker } = DatePicker;
const { Option } = Select;

const beginYear = 1900;

const openResult = (list: string[]) => {
  const args = {
    message: "추천 목록",
    description: list.map((item, index) => `${index + 1}. ${item}`).join("\n"),
    duration: 0,
  };
  notification.open(args);
};

const DataForm: React.FC = () => {
  const [isLoading, setIsLoading] = React.useState(false);
  const [result, setResult] = React.useState<string[]>([]);
  const [form] = Form.useForm();

  const onFinish = (values: any) => {
    console.log("Received values of form: ", values);
    setIsLoading(true);
    fetch("http://localhost:8000/search", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(values),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        setIsLoading(false);
        setResult(data);
        // openResult(data);
      })
      .catch((error) => {
        console.error(error);
        setIsLoading(false);
      });
  };

  return (
    <ConfigProvider locale={locale}>
      <Spin
        spinning={isLoading}
        indicator={<LoadingOutlined style={{ fontSize: 24 }} spin />}
      >
        <Form form={form} onFinish={onFinish}>
          <Form.Item label="출생 연도" name="age" rules={[{ required: true }]}>
            <Select>
              {Array.from(
                { length: 2021 - beginYear + 1 },
                (x, i) => i + beginYear,
              )
                .reverse()
                .map((year) => (
                  <Option key={year} value={year}>
                    {year}
                  </Option>
                ))}
            </Select>
          </Form.Item>
          <Form.Item label="성별" name="gender" rules={[{ required: true }]}>
            <Radio.Group>
              <Radio value="male">남</Radio>
              <Radio value="female">여</Radio>
              <Radio value="etc">기타</Radio>
            </Radio.Group>
          </Form.Item>
          <Form.Item label="지역" name="city" rules={[{ required: true }]}>
            <Select showSearch>
              {locations.map(({ text, value }) => (
                <Option key={value} value={value}>
                  {text}
                </Option>
              ))}
            </Select>
          </Form.Item>
          <Form.Item label="기간" name="daterange" rules={[{ required: true }]}>
            <RangePicker format="YYYY-MM-DD A hh시" showTime />
          </Form.Item>
          <Form.Item shouldUpdate>
            {() => (
              <Button
                type="primary"
                htmlType="submit"
                disabled={
                  !form.isFieldsTouched(true) ||
                  !!form.getFieldsError().filter(({ errors }) => errors.length)
                    .length
                }
              >
                검색
              </Button>
            )}
          </Form.Item>
        </Form>
      </Spin>
      <List
        bordered
        dataSource={result.map((item, index) => `${index + 1}. ${item}`)}
        renderItem={(item) => <List.Item>{item}</List.Item>}
      />
    </ConfigProvider>
  );
};

export default DataForm;
