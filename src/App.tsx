import { lazy, Suspense } from "react";
import "./App.css";

const CharacterModel = lazy(() => import("./components/Character"));
const MainContainer = lazy(() => import("./components/MainContainer"));
const TestCharacter = lazy(() => import("./components/TestCharacter"));
import { LoadingProvider } from "./context/LoadingProvider";

const App = () => {
  // Check if /test route
  const isTestPage = window.location.pathname === "/test";

  if (isTestPage) {
    return (
      <Suspense fallback={<div style={{ color: "white", padding: 20 }}>Loading Test...</div>}>
        <TestCharacter />
      </Suspense>
    );
  }

  return (
    <>
      <LoadingProvider>
        <Suspense>
          <MainContainer>
            <Suspense>
              <CharacterModel />
            </Suspense>
          </MainContainer>
        </Suspense>
      </LoadingProvider>
    </>
  );
};

export default App;
