import { useState, useRef, useEffect } from "react";
import "./App.css";

const API_URL = "http://localhost:8001";

function App() {
  const [token, setToken] = useState(localStorage.getItem("saarthi_token") || null);
  const [name, setName] = useState(localStorage.getItem("saarthi_name") || "");

  if (!token) {
    return <AuthScreen onAuth={(t, n) => {
      setToken(t);
      setName(n);
      localStorage.setItem("saarthi_token", t);
      localStorage.setItem("saarthi_name", n || "");
    }} />;
  }

  return (
    <ChatScreen
      token={token}
      name={name}
      onLogout={() => {
        setToken(null);
        setName("");
        localStorage.removeItem("saarthi_token");
        localStorage.removeItem("saarthi_name");
      }}
    />
  );
}

function AuthScreen({ onAuth }) {
  const [mode, setMode] = useState("login"); // "login" | "register"
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const submit = async () => {
    setError("");
    setLoading(true);
    try {
      const endpoint = mode === "login" ? "/login" : "/register";
      const body = mode === "login" ? { email, password } : { email, password, name };

      const res = await fetch(`${API_URL}${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });

      const data = await res.json();

      if (!res.ok) {
        setError(data.detail || "Something went wrong");
        return;
      }

      onAuth(data.access_token, data.name);
    } catch (err) {
      setError("Couldn't reach the server.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-screen">
      <div className="auth-card">
        <div className="auth-avatar">S</div>
        <h2>Saarthi</h2>
        <p className="auth-subtitle">
          {mode === "login" ? "Welcome back" : "Create your account"}
        </p>

        {mode === "register" && (
          <input
            placeholder="Your name"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
        )}
        <input
          placeholder="Email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          placeholder="Password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        {error && <div className="auth-error">{error}</div>}

        <button onClick={submit} disabled={loading}>
          {loading ? "Please wait..." : mode === "login" ? "Log in" : "Register"}
        </button>

        <div className="auth-switch">
          {mode === "login" ? (
            <>Don't have an account? <span onClick={() => setMode("register")}>Register</span></>
          ) : (
            <>Already have an account? <span onClick={() => setMode("login")}>Log in</span></>
          )}
        </div>
      </div>
    </div>
  );
}

function ChatScreen({ token, name, onLogout }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const endRef = useRef(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const timestamp = () =>
    new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });

  const sendMessage = async () => {
    if (!input.trim()) return;
    const userMsg = { role: "user", content: input, time: timestamp() };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ message: userMsg.content }),
      });

      if (res.status === 401) {
        onLogout();
        return;
      }

      const data = await res.json();
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: data.reply, time: timestamp() },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "⚠️ Couldn't reach Saarthi's server.", time: timestamp() },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-app">
      <div className="chat-header">
        <div className="avatar">S</div>
        <div style={{ flex: 1 }}>
          <div className="chat-title">Saarthi</div>
          <div className="chat-subtitle">{loading ? "typing..." : "online"}</div>
        </div>
        <button className="logout-btn" onClick={onLogout}>Logout</button>
      </div>

      <div className="chat-body">
        {messages.length === 0 && (
          <div className="empty-state">
            {name ? `Hi ${name}, say hi to Saarthi to start.` : "Say hi to Saarthi to start the conversation."}
          </div>
        )}
        {messages.map((m, i) => (
          <div key={i} className={`bubble-row ${m.role}`}>
            <div className={`bubble ${m.role}`}>
              <div className="bubble-text">{m.content}</div>
              <div className="bubble-time">{m.time}</div>
            </div>
          </div>
        ))}
        {loading && (
          <div className="bubble-row assistant">
            <div className="bubble assistant typing">
              <span></span><span></span><span></span>
            </div>
          </div>
        )}
        <div ref={endRef} />
      </div>

      <div className="chat-input-bar">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          placeholder="Type a message"
        />
        <button onClick={sendMessage} disabled={!input.trim()}>
          ➤
        </button>
      </div>
    </div>
  );
}

export default App;