import React, { useEffect, useState } from 'react';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, LabelList,Cell,
} from 'recharts';

const METRIC_DESCRIPTIONS = {
  ks_stat: {
    label: "Kolmogorov-Smirnov Statistic (KS Stat)",
    desc: "Measures the maximum difference between the distributions of real and synthetic numerical data. Lower is better; ideal < 0.3.",
  },
  wasserstein_distance: {
    label: "Wasserstein Distance",
    desc: "Measures the distance between distributions of numerical features. Lower values indicate synthetic data closely matches real data. Ideal depends on data, usually < 10.",
  },
  chi2_stat: {
    label: "Chi-Square Statistic",
    desc: "Tests distribution similarity of categorical features. Lower values mean better similarity. Ideal < 10.",
  },
  p_value: {
    label: "P-Value",
    desc: "Probability the observed similarity is by chance. Higher values mean synthetic and real data are statistically similar. Ideal > 0.05.",
  },
  tvd: {
    label: "Total Variation Distance (TVD)",
    desc: "Measures how much the categorical distributions differ. Lower values are better. Ideal < 0.2.",
  },
  average_correlation_difference: {
    label: "Average Correlation Difference",
    desc: "Shows average difference between correlation matrices of real and synthetic data. Lower means better. Ideal < 0.15.",
  },
  "Pairwise Correlation Difference": {
    label: "Pairwise Correlation Differences",
    desc: "Difference between each pair of features' correlations in real vs synthetic data. Lower means better. Ideal < 0.15.",
  },
};

export default function Validation() {
  const [validationData, setValidationData] = useState(null);

  useEffect(() => {
    fetch(`${process.env.REACT_APP_API_URL}/get-validation-results`)
      .then(res => res.json())
      .then(setValidationData)
      .catch(err => console.error("Error fetching validation results:", err));
  }, []);

  const downloadFile = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/download-output`);
      if (!response.ok) {
        alert("Failed to download file");
        return;
      }
      const blob = await response.blob();
      const contentDisposition = response.headers.get("Content-Disposition");
      const filenameMatch = contentDisposition && contentDisposition.match(/filename="?(.+)"?/);
      const filename = filenameMatch ? filenameMatch[1] : 'synthetic_output.csv';

      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      alert("An error occurred while downloading the file.");
      console.error(err);
    }
  };

  // Helper: truncate to 2 decimals (for tooltip only, bars show no label)
  const formatValue = (val) => (typeof val === "number" ? val.toFixed(2) : val);

  // Render a single BarChart for a metric
  const renderBarChart = (metricKey, data, threshold) => {
    const labels = Object.keys(data);
    const values = Object.values(data);

    // Get label and description for metric
    const metricInfo = METRIC_DESCRIPTIONS[metricKey] || { label: metricKey, desc: "" };

    return (
      <div className="my-8" key={metricKey}>
        <h3 className="text-xl font-semibold mb-1">{metricInfo.label}</h3>
        {metricInfo.desc && <p className="text-sm italic text-gray-600 mb-3 max-w-2xl">{metricInfo.desc}</p>}

        <ResponsiveContainer width="100%" height={300}>
          <BarChart
            data={labels.map((label, i) => ({ name: label, value: values[i] }))}
            margin={{ top: 20, right: 30, left: 20, bottom: 80 }}
          >
            <XAxis
              dataKey="name"
              angle={-90}
              textAnchor="end"
              interval={0}
              height={100}
              tick={{ fontSize: 12 }}
            />
            <YAxis />
            <Tooltip formatter={formatValue} />
            <Bar
              dataKey="value"
              fill="#22c55e"
              isAnimationActive={false}
              // Color red if above threshold, else green
              // If no threshold, all green
              fillOpacity={1}
              // For coloring bars red or green based on threshold:
              // recharts supports fill as function via "fill" prop replaced by fill prop on <Cell>
            >
              {labels.map((label, i) => (
                <Cell
                  key={`cell-${i}`}
                  fill={
                    threshold !== undefined && values[i] > threshold
                      ? "#ef4444" // red
                      : "#22c55e" // green
                  }
                />
              ))}
              {/* Remove label on bars */}
              {/* <LabelList dataKey="value" position="top" formatter={formatValue} /> */}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    );
  };

  const renderCharts = () => {
    if (!validationData) return <p>Loading...</p>;

    if (validationData?.message === "Validation not applicable for this mode.") {
      return (
        <div className="text-gray-600 text-lg italic mt-6">
          ⚠️ Validation results are not applicable for this generation mode.
        </div>
      );
    }

    const perColumnStats = {};
    const thresholds = {
      ks_stat: 0.3,
      wasserstein_distance: 10,
      chi2_stat: 10,
      p_value: null, // no threshold for p-value; higher is better
      tvd: 0.2,
      average_correlation_difference: 0.15,
    };

    for (const [col, metrics] of Object.entries(validationData)) {
      if (col === "_pairwise_correlation") continue;
      for (const [metric, value] of Object.entries(metrics)) {
        // Only add numbers and skip nulls
        if (typeof value === 'number') {
          if (!perColumnStats[metric]) perColumnStats[metric] = {};
          perColumnStats[metric][col] = value;
        }
      }
    }

    // Build charts for each metric except p_value (show as separate chart)
    const charts = Object.entries(perColumnStats)
      .filter(([metric]) => metric !== "p_value") // skip p_value for now
      .map(([metric, values]) => renderBarChart(metric, values, thresholds[metric]));

    // Add p_value chart separately because ideal is high values
    if (perColumnStats["p_value"]) {
      charts.push(renderBarChart("p_value", perColumnStats["p_value"], null));
    }

    // Pairwise correlation
    const pairwise = validationData._pairwise_correlation?.per_feature_difference || {};
    const flattened = {};
    Object.entries(pairwise).forEach(([col1, sub]) => {
      Object.entries(sub).forEach(([col2, val]) => {
        flattened[`${col1} vs ${col2}`] = val;
      });
    });
    charts.push(renderBarChart("Pairwise Correlation Difference", flattened, 0.15));

    // Similarity score
    const similarityScore = 1 - (validationData._pairwise_correlation?.average_correlation_difference || 0);

    return (
      <div className="space-y-4">
        <div className="text-xl font-bold mt-6 mb-4">
          📈 Dataset Similarity Score: {similarityScore.toFixed(4)}
        </div>
        {charts}
      </div>
    );
  };

  return (
    <div className="p-10 max-w-5xl mx-auto space-y-8">
      <h2 className="text-3xl font-bold">Validation Results</h2>
      <p>Here’s how your synthetic data compares to your real data...</p>
      {renderCharts()}
      <button
        onClick={downloadFile}
        className="bg-#7B61FF text-white px-6 py-2 rounded-xl"
      >
        Save
      </button>
    </div>
  );
}