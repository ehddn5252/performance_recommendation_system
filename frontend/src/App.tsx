import React from "react";
import "./App.css";
import "antd/dist/antd.css";
import { Layout } from "antd";
import "moment/locale/ko";
import DataForm from "./DataForm";

const { Content } = Layout;

const App: React.FC = () => {
  return (
    <Layout>
      <div className="container">
        <Content className="wrapper">
          <DataForm />
        </Content>
      </div>
    </Layout>
  );
};

export default App;
